# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20190501


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AuthenticationServerPolicy(object):
    """
    Policy for the details regarding each authentication server under dynamic authentication. We specify the value of selectors for which this authentication server must be selected for a request under keys. We specify the configuration details of authentication server under authenticationServerDetail.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AuthenticationServerPolicy object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key:
            The value to assign to the key property of this AuthenticationServerPolicy.
        :type key: oci.apigateway.models.DynamicSelectionKey

        :param authentication_server_detail:
            The value to assign to the authentication_server_detail property of this AuthenticationServerPolicy.
        :type authentication_server_detail: oci.apigateway.models.AuthenticationPolicy

        """
        self.swagger_types = {
            'key': 'DynamicSelectionKey',
            'authentication_server_detail': 'AuthenticationPolicy'
        }
        self.attribute_map = {
            'key': 'key',
            'authentication_server_detail': 'authenticationServerDetail'
        }
        self._key = None
        self._authentication_server_detail = None

    @property
    def key(self):
        """
        **[Required]** Gets the key of this AuthenticationServerPolicy.

        :return: The key of this AuthenticationServerPolicy.
        :rtype: oci.apigateway.models.DynamicSelectionKey
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this AuthenticationServerPolicy.

        :param key: The key of this AuthenticationServerPolicy.
        :type: oci.apigateway.models.DynamicSelectionKey
        """
        self._key = key

    @property
    def authentication_server_detail(self):
        """
        **[Required]** Gets the authentication_server_detail of this AuthenticationServerPolicy.

        :return: The authentication_server_detail of this AuthenticationServerPolicy.
        :rtype: oci.apigateway.models.AuthenticationPolicy
        """
        return self._authentication_server_detail

    @authentication_server_detail.setter
    def authentication_server_detail(self, authentication_server_detail):
        """
        Sets the authentication_server_detail of this AuthenticationServerPolicy.

        :param authentication_server_detail: The authentication_server_detail of this AuthenticationServerPolicy.
        :type: oci.apigateway.models.AuthenticationPolicy
        """
        self._authentication_server_detail = authentication_server_detail

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
