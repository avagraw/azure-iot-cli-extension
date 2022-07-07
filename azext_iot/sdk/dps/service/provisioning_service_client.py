# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Serializer, Deserializer
from msrestazure import AzureConfiguration
from .version import VERSION
from .operations.certificate_authority_operations import CertificateAuthorityOperations
from .operations.individual_enrollment_operations import IndividualEnrollmentOperations
from .operations.enrollment_group_operations import EnrollmentGroupOperations
from .operations.device_registration_state_operations import DeviceRegistrationStateOperations
from .operations.trust_bundle_operations import TrustBundleOperations
from . import models


class ProvisioningServiceClientConfiguration(AzureConfiguration):
    """Configuration for ProvisioningServiceClient
    Note that all parameters used to create this instance are saved as instance
    attributes.

    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param str base_url: Service URL
    """

    def __init__(
            self, credentials, base_url=None):

        if credentials is None:
            raise ValueError("Parameter 'credentials' must not be None.")
        if not base_url:
            base_url = 'https://your-dps.azure-devices-provisioning.net'

        super(ProvisioningServiceClientConfiguration, self).__init__(base_url)

        self.add_user_agent('service/{}'.format(VERSION))
        self.add_user_agent('Azure-SDK-For-Python')

        self.credentials = credentials


class ProvisioningServiceClient(SDKClient):
    """API for service operations with the Azure IoT Hub Device Provisioning Service

    :ivar config: Configuration for client.
    :vartype config: ProvisioningServiceClientConfiguration

    :ivar certificate_authority: CertificateAuthority operations
    :vartype certificate_authority: dps.operations.CertificateAuthorityOperations
    :ivar individual_enrollment: IndividualEnrollment operations
    :vartype individual_enrollment: dps.operations.IndividualEnrollmentOperations
    :ivar enrollment_group: EnrollmentGroup operations
    :vartype enrollment_group: dps.operations.EnrollmentGroupOperations
    :ivar device_registration_state: DeviceRegistrationState operations
    :vartype device_registration_state: dps.operations.DeviceRegistrationStateOperations
    :ivar trust_bundle: TrustBundle operations
    :vartype trust_bundle: dps.operations.TrustBundleOperations

    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param str base_url: Service URL
    """

    def __init__(
            self, credentials, base_url=None):

        self.config = ProvisioningServiceClientConfiguration(credentials, base_url)
        super(ProvisioningServiceClient, self).__init__(self.config.credentials, self.config)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.api_version = '2021-11-01-preview'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.certificate_authority = CertificateAuthorityOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.individual_enrollment = IndividualEnrollmentOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.enrollment_group = EnrollmentGroupOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.device_registration_state = DeviceRegistrationStateOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.trust_bundle = TrustBundleOperations(
            self._client, self.config, self._serialize, self._deserialize)
