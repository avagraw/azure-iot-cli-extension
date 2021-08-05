# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import pytest
from time import sleep
from knack.util import CLIError

from azext_iot.tests import IoTLiveScenarioTest
from azext_iot.tests.settings import DynamoSettings, ENV_SET_TEST_IOTHUB_REQUIRED, ENV_SET_TEST_IOTHUB_OPTIONAL, UserTypes
from azext_iot.common.utility import ensure_iothub_sdk_min_version

from azext_iot.tests.generators import generate_generic_id
# TODO: assert DEVICE_DEVICESCOPE_PREFIX format in parent device twin.
from azext_iot.constants import IOTHUB_TRACK_2_SDK_MIN_VERSION
from azext_iot.tests import DEFAULT_CONTAINER
from azure.cli.core._profile import Profile
from azure.cli.core.mock import DummyCli

opt_env_set = ENV_SET_TEST_IOTHUB_OPTIONAL + ["azext_iot_identity_teststorageid"]

settings = DynamoSettings(
    req_env_set=ENV_SET_TEST_IOTHUB_REQUIRED, opt_env_set=opt_env_set
)
LIVE_STORAGE_ACCOUNT = settings.env.azext_iot_teststorageaccount

# Set this environment variable to enable identity-based integration tests
# You will need permissions to add and remove role assignments for this storage account
LIVE_STORAGE_RESOURCE_ID = settings.env.azext_iot_identity_teststorageid
STORAGE_ROLE = "Storage Blob Data Contributor"

CWD = os.path.dirname(os.path.abspath(__file__))

user_managed_identity_name = generate_generic_id()


class TestIoTStorage(IoTLiveScenarioTest):
    def __init__(self, test_case):

        super(TestIoTStorage, self).__init__(test_case)
        self.managed_identity = None

        profile = Profile(cli_ctx=DummyCli())
        subscription = profile.get_subscription()
        self.user = subscription["user"]

        if LIVE_STORAGE_ACCOUNT:
            self.live_storage_uri = self.get_container_sas_url()

    def get_container_sas_url(self):
        from datetime import datetime, timedelta
        from azure.storage.blob import ResourceTypes, AccountSasPermissions, generate_account_sas, BlobServiceClient

        storage_account_connenction = self.cmd(
            "storage account show-connection-string --name {}".format(
                LIVE_STORAGE_ACCOUNT
            )
        ).get_output_in_json()

        blob_service_client = BlobServiceClient.from_connection_string(conn_str=storage_account_connenction["connectionString"])

        sas_token = generate_account_sas(
            blob_service_client.account_name,
            account_key=blob_service_client.credential.account_key,
            resource_types=ResourceTypes(object=True),
            permission=AccountSasPermissions(
                read=True, add=True, create=True, delete=True, filter=True, list=True, update=True, write=True
            ),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )

        container_name = (
            settings.env.azext_iot_teststoragecontainer if settings.env.azext_iot_teststoragecontainer else DEFAULT_CONTAINER
        )

        container_sas_url = "https://" + LIVE_STORAGE_ACCOUNT + ".blob.core.windows.net" + "/" + container_name + "?" + sas_token

        return container_sas_url

    def get_managed_identity(self):
        # Check if there is a managed identity already
        if self.managed_identity:
            return self.managed_identity

        # Create managed identity
        result = self.cmd(
            "identity create -n {} -g {}".format(
                user_managed_identity_name, self.entity_rg
            )).get_output_in_json()

        # ensure resource is created before hub immediately tries to assign it
        sleep(10)

        self.managed_identity = result
        return self.managed_identity

    def assign_storage_role(self, assignee):
        if self.user["type"] == UserTypes.user.value:
            self.cmd(
                'role assignment create --assignee"{}" --role "{}" --scope "{}"'.format(
                    assignee, STORAGE_ROLE, LIVE_STORAGE_RESOURCE_ID
                )
            )
        elif self.user["type"] == UserTypes.servicePrincipal.value:
            self.cmd(
                'role assignment create --assignee-object-id "{}" --role "{}" --scope "{}" --assignee-principal-type "{}"'.format(
                    assignee, STORAGE_ROLE, LIVE_STORAGE_RESOURCE_ID, "ServicePrincipal"
                )
            )
        else:
            userType = self.user["type"]
            raise CLIError(f"User type {userType} not supported. Can't run test(s).")

        # give time to finish job
        sleep(60)

    def tearDown(self):
        if self.managed_identity:
            self.cmd('identity delete -n {} -g {}'.format(
                user_managed_identity_name, self.entity_rg
            ))
        return super().tearDown()

    @pytest.mark.skipif(
        not LIVE_STORAGE_ACCOUNT, reason="empty azext_iot_teststorageaccount env var"
    )
    def test_storage(self):
        device_count = 1

        content_path = os.path.join(CWD, "test_generic_replace.json")
        device_ids = self.generate_device_names(device_count)

        self.cmd(
            "iot hub device-identity create -d {} -n {} -g {} --ee".format(
                device_ids[0], self.entity_name, self.entity_rg
            ),
            checks=[self.check("deviceId", device_ids[0])],
        )

        self.cmd(
            'iot device upload-file -d {} -n {} --fp "{}" --ct {}'.format(
                device_ids[0], self.entity_name, content_path, "application/json"
            ),
            checks=self.is_empty(),
        )

        # With connection string
        self.cmd(
            'iot device upload-file -d {} --login {} --fp "{}" --ct {}'.format(
                device_ids[0], self.connection_string, content_path, "application/json"
            ),
            checks=self.is_empty(),
        )

        self.cmd(
            'iot hub device-identity export -n {} --bcu "{}"'.format(
                self.entity_name, self.live_storage_uri
            ),
            checks=[
                self.check("outputBlobContainerUri", self.live_storage_uri),
                self.check("failureReason", None),
                self.check("type", "export"),
                self.check("excludeKeysInExport", True),
                self.exists("jobId"),
            ],
        )

        # give time to finish job
        sleep(30)

        self.cmd(
            'iot hub device-identity export -n {} --bcu "{}" --auth-type {} --ik true'.format(
                self.entity_name, self.live_storage_uri, "key"
            ),
            checks=[
                self.check("outputBlobContainerUri", self.live_storage_uri),
                self.check("failureReason", None),
                self.check("type", "export"),
                self.check("excludeKeysInExport", False),
                self.exists("jobId"),
            ],
        )

        # give time to finish job
        sleep(30)

        self.cmd(
            'iot hub device-identity import -n {} --ibcu "{}" --obcu "{}" --auth-type {}'.format(
                self.entity_name, self.live_storage_uri, self.live_storage_uri, "key"
            ),
            checks=[
                self.check("outputBlobContainerUri", self.live_storage_uri),
                self.check("inputBlobContainerUri", self.live_storage_uri),
                self.check("failureReason", None),
                self.check("type", "import"),
                self.check("storageAuthenticationType", "keyBased"),
                self.exists("jobId"),
            ],
        )

    @pytest.mark.skipif(
        not all([LIVE_STORAGE_RESOURCE_ID, LIVE_STORAGE_ACCOUNT]),
        reason="azext_iot_identity_teststorageid and azext_iot_teststorageaccount env vars not set",
    )
    @pytest.mark.skipif(
        not ensure_iothub_sdk_min_version(IOTHUB_TRACK_2_SDK_MIN_VERSION),
        reason="Skipping track 2 tests because SDK is track 1")
    def test_system_identity_storage(self):
        identity_type_enable = "SystemAssigned"

        # check hub identity
        identity_enabled = False

        hub_identity = self.cmd(
            "iot hub identity show -n {}".format(self.entity_name)
        ).get_output_in_json()

        if identity_type_enable not in hub_identity.get("type", None):
            # enable hub identity and get ID
            hub_identity = self.cmd(
                "iot hub identity assign -n {} --system".format(
                    self.entity_name,
                )
            ).get_output_in_json()

            identity_enabled = True

        # principal id for system assigned user identity
        hub_id = hub_identity.get("principalId", None)
        assert hub_id

        # setup RBAC for storage account
        storage_account_roles = self.cmd(
            'role assignment list --scope "{}" --role "{}" --query "[].principalId"'.format(
                LIVE_STORAGE_RESOURCE_ID, STORAGE_ROLE
            )
        ).get_output_in_json()

        if hub_id not in storage_account_roles:
            self.assign_storage_role(hub_id)

        self.cmd(
            'iot hub device-identity export -n {} --bcu "{}" --auth-type {} --identity {} --ik true'.format(
                self.entity_name, self.live_storage_uri, "identity", "[system]"
            ),
            checks=[
                self.check("outputBlobContainerUri", self.live_storage_uri),
                self.check("failureReason", None),
                self.check("type", "export"),
                self.check("excludeKeysInExport", False),
                self.check("storageAuthenticationType", "identityBased"),
                self.exists("jobId"),
            ],
        )

        self.cmd(
            'iot hub device-identity import -n {} --ibcu "{}" --obcu "{}" --auth-type {} --identity {}'.format(
                self.entity_name, self.live_storage_uri, self.live_storage_uri, "identity", "[system]"
            ),
            checks=[
                self.check("outputBlobContainerUri", self.live_storage_uri),
                self.check("inputBlobContainerUri", self.live_storage_uri),
                self.check("failureReason", None),
                self.check("type", "import"),
                self.check("storageAuthenticationType", "identityBased"),
                self.exists("jobId"),
            ],
        )

        self.cmd(
            'iot hub device-identity export -n {} --bcu "{}" --auth-type {} --identity {}'.format(
                self.entity_name, self.live_storage_uri, "identity", "fake_managed_identity"
            ),
            expect_failure=True
        )

        # if we enabled identity for this hub, undo identity and RBAC
        if identity_enabled:
            # delete role assignment first, disabling identity removes the assignee ID from AAD
            self.cmd(
                'role assignment delete --assignee "{}" --role "{}" --scope "{}"'.format(
                    hub_id, STORAGE_ROLE, LIVE_STORAGE_RESOURCE_ID
                )
            )
            self.cmd(
                "iot hub identity remove -n {} --system".format(
                    self.entity_name
                )
            )

    @pytest.mark.skipif(
        not all([LIVE_STORAGE_RESOURCE_ID, LIVE_STORAGE_ACCOUNT]),
        reason="azext_iot_identity_teststorageid and azext_iot_teststorageaccount env vars not set",
    )
    @pytest.mark.skipif(
        not ensure_iothub_sdk_min_version(IOTHUB_TRACK_2_SDK_MIN_VERSION),
        reason="Skipping track 2 tests because SDK is track 1")
    def test_user_identity_storage(self):
        # User Assigned Managed Identity
        user_identity = self.get_managed_identity()
        identity_id = user_identity["id"]
        # check hub identity
        identity_enabled = False
        hub_identity = self.cmd(
            "iot hub identity show -n {}".format(self.entity_name)
        ).get_output_in_json()

        if hub_identity.get("userAssignedIdentities", None) != user_identity["principalId"]:
            # enable hub identity and get ID
            hub_identity = self.cmd(
                "iot hub identity assign -n {} --user {}".format(
                    self.entity_name, identity_id
                )
            ).get_output_in_json()

            identity_enabled = True

        identity_principal = hub_identity["userAssignedIdentities"][identity_id]["principalId"]
        assert identity_principal == user_identity["principalId"]

        # setup RBAC for storage account
        storage_account_roles = self.cmd(
            'role assignment list --scope "{}" --role "{}" --query "[].principalId"'.format(
                LIVE_STORAGE_RESOURCE_ID, STORAGE_ROLE
            )
        ).get_output_in_json()

        if identity_principal not in storage_account_roles:
            self.assign_storage_role(identity_principal)

        # identity-based device-identity export
        self.cmd(
            'iot hub device-identity export -n {} --bcu "{}" --auth-type {} --identity {} --ik true'.format(
                self.entity_name, self.live_storage_uri, "identity", identity_id
            ),
            checks=[
                self.check("outputBlobContainerUri", self.live_storage_uri),
                self.check("failureReason", None),
                self.check("type", "export"),
                self.check("excludeKeysInExport", False),
                self.check("storageAuthenticationType", "identityBased"),
                self.exists("jobId"),
            ],
        )

        # give time to finish job
        sleep(30)

        self.cmd(
            'iot hub device-identity import -n {} --ibcu "{}" --obcu "{}" --auth-type {} --identity {}'.format(
                self.entity_name, self.live_storage_uri, self.live_storage_uri, "identity", identity_id
            ),
            checks=[
                self.check("outputBlobContainerUri", self.live_storage_uri),
                self.check("inputBlobContainerUri", self.live_storage_uri),
                self.check("failureReason", None),
                self.check("type", "import"),
                self.check("storageAuthenticationType", "identityBased"),
                self.exists("jobId"),
            ],
        )

        self.cmd(
            'iot hub device-identity export -n {} --bcu "{}" --auth-type {} --identity {}'.format(
                self.entity_name, self.live_storage_uri, "identity", "fake_managed_identity"
            ),
            expect_failure=True
        )

        # if we enabled identity for this hub, undo identity and RBAC
        if identity_enabled:
            # delete role assignment first, disabling identity removes the assignee ID from AAD
            self.cmd(
                'role assignment delete --assignee "{}" --role "{}" --scope "{}"'.format(
                    identity_principal, STORAGE_ROLE, LIVE_STORAGE_RESOURCE_ID
                )
            )
            self.cmd(
                "iot hub identity remove -n {} --user".format(
                    self.entity_name
                )
            )

        self.tearDown()
