# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


from typing import List
from knack.util import CLIError
from knack.log import get_logger
from azext_iot.constants import CENTRAL_ENDPOINT
from azext_iot.central import services as central_services
from azext_iot.central.models.v1_1_preview import OrganizationV1_1_preview

logger = get_logger(__name__)


class CentralOrganizationProvider:
    def __init__(self, cmd, app_id: str, api_version: str, token=None):
        """
        Provider for organizations APIs

        Args:
            cmd: command passed into az
            app_id: name of app (used for forming request URL)
            api_version: API version (appendend to request URL)
            token: (OPTIONAL) authorization token to fetch device details from IoTC.
                MUST INCLUDE type (e.g. 'SharedAccessToken ...', 'Bearer ...')
                Useful in scenarios where user doesn't own the app
                therefore AAD token won't work, but a SAS token generated by owner will
        """
        self._cmd = cmd
        self._app_id = app_id
        self._token = token
        self._api_version = api_version
        self._orgs = {}

    def list_organizations(
        self, central_dns_suffix=CENTRAL_ENDPOINT
    ) -> List[OrganizationV1_1_preview]:
        orgs = central_services.organization.list_orgs(
            cmd=self._cmd,
            app_id=self._app_id,
            token=self._token,
            central_dns_suffix=central_dns_suffix,
            api_version=self._api_version,
        )

        # add to cache
        self._orgs.update({org.id: org for org in orgs})

        return orgs

    def get_organization(
        self,
        org_id,
        central_dns_suffix=CENTRAL_ENDPOINT,
    ) -> OrganizationV1_1_preview:
        # get or add to cache
        org = self._orgs.get(org_id)
        if not org:
            org = central_services.organization.get_org(
                cmd=self._cmd,
                app_id=self._app_id,
                org_id=org_id,
                token=self._token,
                central_dns_suffix=central_dns_suffix,
                api_version=self._api_version,
            )
            self._orgs[org_id] = org

        if not org:
            raise CLIError("No organization found with id: '{}'.".format(org_id))

        return org

    def delete_organization(
        self,
        org_id,
        central_dns_suffix=CENTRAL_ENDPOINT,
    ) -> OrganizationV1_1_preview:
        # get or add to cache
        org = central_services.organization.delete_org(
            cmd=self._cmd,
            app_id=self._app_id,
            org_id=org_id,
            token=self._token,
            central_dns_suffix=central_dns_suffix,
            api_version=self._api_version,
        )

        return org

    def create_or_update_organization(
        self,
        org_id,
        org_name,
        parent_org,
        update=False,
        central_dns_suffix=CENTRAL_ENDPOINT,
    ):
        if org_id in self._orgs:
            raise CLIError("Organization already exists")
        org = central_services.organization.create_or_update_org(
            self._cmd,
            self._app_id,
            org_id=org_id,
            org_name=org_name,
            parent_org=parent_org,
            token=self._token,
            update=update,
            api_version=self._api_version,
            central_dns_suffix=central_dns_suffix,
        )

        if not org:
            raise CLIError(
                "Failed to create organization with id: '{}'.".format(org_id)
            )

        # add to cache
        self._orgs[org.id] = org

        return org
