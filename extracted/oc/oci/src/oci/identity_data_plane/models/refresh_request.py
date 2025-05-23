# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: v1


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RefreshRequest(object):
    """
    RefreshRequest model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RefreshRequest object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param current_token:
            The value to assign to the current_token property of this RefreshRequest.
        :type current_token: str

        :param new_public_key:
            The value to assign to the new_public_key property of this RefreshRequest.
        :type new_public_key: str

        """
        self.swagger_types = {
            'current_token': 'str',
            'new_public_key': 'str'
        }
        self.attribute_map = {
            'current_token': 'currentToken',
            'new_public_key': 'newPublicKey'
        }
        self._current_token = None
        self._new_public_key = None

    @property
    def current_token(self):
        """
        **[Required]** Gets the current_token of this RefreshRequest.
        The current security token that is to be renewed.


        :return: The current_token of this RefreshRequest.
        :rtype: str
        """
        return self._current_token

    @current_token.setter
    def current_token(self, current_token):
        """
        Sets the current_token of this RefreshRequest.
        The current security token that is to be renewed.


        :param current_token: The current_token of this RefreshRequest.
        :type: str
        """
        self._current_token = current_token

    @property
    def new_public_key(self):
        """
        Gets the new_public_key of this RefreshRequest.
        An optional new public for the new token. If not supplied, currentToken's public key will be used.


        :return: The new_public_key of this RefreshRequest.
        :rtype: str
        """
        return self._new_public_key

    @new_public_key.setter
    def new_public_key(self, new_public_key):
        """
        Sets the new_public_key of this RefreshRequest.
        An optional new public for the new token. If not supplied, currentToken's public key will be used.


        :param new_public_key: The new_public_key of this RefreshRequest.
        :type: str
        """
        self._new_public_key = new_public_key

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
