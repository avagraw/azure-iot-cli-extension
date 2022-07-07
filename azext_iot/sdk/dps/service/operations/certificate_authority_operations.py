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

import uuid
from msrest.pipeline import ClientRawResponse

from .. import models


class CertificateAuthorityOperations(object):
    """CertificateAuthorityOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    :ivar api_version: The API version to use for the request. Supported versions include: 2021-11-01-preview. Constant value: "2021-11-01-preview".
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self.api_version = "2021-11-01-preview"

        self.config = config

    def get(
            self, id, custom_headers=None, raw=False, **operation_config):
        """Get a certificate authority. This operation requires the
        certificateAuthorities/read permission.

        :param id: The certificate authority id. A case-insensitive string (up
         to 128 characters long) of alphanumeric characters plus certain
         special characters : . _ -. No special characters allowed at start or
         end.
        :type id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: CertificateAuthority or ClientRawResponse if raw=true
        :rtype: ~dps.models.CertificateAuthority or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ProvisioningServiceErrorDetailsException<dps.models.ProvisioningServiceErrorDetailsException>`
        """
        # Construct URL
        url = self.get.metadata['url']
        path_format_arguments = {
            'id': self._serialize.url("id", id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ProvisioningServiceErrorDetailsException(self._deserialize, response)

        deserialized = None
        header_dict = {}

        if response.status_code == 200:
            deserialized = self._deserialize('CertificateAuthority', response)
            header_dict = {
                'ETag': 'str',
                'x-ms-error-code': 'str',
            }

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            client_raw_response.add_headers(header_dict)
            return client_raw_response

        return deserialized
    get.metadata = {'url': '/certificateAuthorities/{id}'}

    def create_or_update(
            self, id, certificate_authority, if_match=None, custom_headers=None, raw=False, **operation_config):
        """Create or replace a certificate authority with the specified
        certificate authority source type. This operation requires the
        certificateAuthorities/write permission.

        :param id: The desired certificate authority name. A case-insensitive
         string (up to 128 characters long) of alphanumeric characters plus
         certain special characters : . _ -. No special characters allowed at
         start or end.
        :type id: str
        :param certificate_authority: The created certificate authority
         object.
        :type certificate_authority: ~dps.models.CertificateAuthority
        :param if_match: The ETag of the certificate authority.
        :type if_match: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: CertificateAuthority or ClientRawResponse if raw=true
        :rtype: ~dps.models.CertificateAuthority or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ProvisioningServiceErrorDetailsException<dps.models.ProvisioningServiceErrorDetailsException>`
        """
        # Construct URL
        url = self.create_or_update.metadata['url']
        path_format_arguments = {
            'id': self._serialize.url("id", id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if if_match is not None:
            header_parameters['If-Match'] = self._serialize.header("if_match", if_match, 'str')
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct body
        body_content = self._serialize.body(certificate_authority, 'CertificateAuthority')

        # Construct and send request
        request = self._client.put(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ProvisioningServiceErrorDetailsException(self._deserialize, response)

        deserialized = None
        header_dict = {}

        if response.status_code == 200:
            deserialized = self._deserialize('CertificateAuthority', response)
            header_dict = {
                'x-ms-error-code': 'str',
            }

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            client_raw_response.add_headers(header_dict)
            return client_raw_response

        return deserialized
    create_or_update.metadata = {'url': '/certificateAuthorities/{id}'}

    def delete(
            self, id, if_match, custom_headers=None, raw=False, **operation_config):
        """Delete the certificate authority. This operation requires the
        certificateAuthorities/delete permission.

        :param id: The certificate authority name. A case-insensitive string
         (up to 128 characters long) of alphanumeric characters plus certain
         special characters : . _ -. No special characters allowed at start or
         end.
        :type id: str
        :param if_match: The ETag of the certificate authority.
        :type if_match: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or ClientRawResponse if raw=true
        :rtype: None or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ProvisioningServiceErrorDetailsException<dps.models.ProvisioningServiceErrorDetailsException>`
        """
        # Construct URL
        url = self.delete.metadata['url']
        path_format_arguments = {
            'id': self._serialize.url("id", id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        header_parameters['If-Match'] = self._serialize.header("if_match", if_match, 'str')
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.delete(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [204]:
            raise models.ProvisioningServiceErrorDetailsException(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            client_raw_response.add_headers({
                'x-ms-error-code': 'str',
            })
            return client_raw_response
    delete.metadata = {'url': '/certificateAuthorities/{id}'}

    def query(
            self, query, x_ms_max_item_count=None, x_ms_continuation=None, custom_headers=None, raw=False, **operation_config):
        """Retrieves a list of the certificate authorities and a continuation
        token to retrieve the next page. This operation requires the
        certificateAuthorities/read permission.

        :param query:
        :type query: str
        :param x_ms_max_item_count: Page size
        :type x_ms_max_item_count: int
        :param x_ms_continuation: Continuation token
        :type x_ms_continuation: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: list or ClientRawResponse if raw=true
        :rtype: list[~dps.models.CertificateAuthority] or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ProvisioningServiceErrorDetailsException<dps.models.ProvisioningServiceErrorDetailsException>`
        """
        query_specification = models.QuerySpecification(query=query)

        # Construct URL
        url = self.query.metadata['url']

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if x_ms_max_item_count is not None:
            header_parameters['x-ms-max-item-count'] = self._serialize.header("x_ms_max_item_count", x_ms_max_item_count, 'int')
        if x_ms_continuation is not None:
            header_parameters['x-ms-continuation'] = self._serialize.header("x_ms_continuation", x_ms_continuation, 'str')
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct body
        body_content = self._serialize.body(query_specification, 'QuerySpecification')

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ProvisioningServiceErrorDetailsException(self._deserialize, response)

        deserialized = None
        header_dict = {}

        if response.status_code == 200:
            deserialized = self._deserialize('[CertificateAuthority]', response)
            header_dict = {
                'x-ms-continuation': 'str',
                'x-ms-max-item-count': 'int',
                'x-ms-item-type': 'str',
                'x-ms-error-code': 'str',
            }

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            client_raw_response.add_headers(header_dict)
            return client_raw_response

        return deserialized
    query.metadata = {'url': '/certificateAuthorities/query'}
