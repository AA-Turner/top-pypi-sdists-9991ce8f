# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: v1


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class IdentitySettingsTokens(object):
    """
    A list of tokens and their expiry length.
    """

    #: A constant which can be used with the type property of a IdentitySettingsTokens.
    #: This constant has a value of "emailVerification"
    TYPE_EMAIL_VERIFICATION = "emailVerification"

    #: A constant which can be used with the type property of a IdentitySettingsTokens.
    #: This constant has a value of "passwordReset"
    TYPE_PASSWORD_RESET = "passwordReset"

    #: A constant which can be used with the type property of a IdentitySettingsTokens.
    #: This constant has a value of "createUser"
    TYPE_CREATE_USER = "createUser"

    def __init__(self, **kwargs):
        """
        Initializes a new IdentitySettingsTokens object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param expires_after:
            The value to assign to the expires_after property of this IdentitySettingsTokens.
        :type expires_after: int

        :param type:
            The value to assign to the type property of this IdentitySettingsTokens.
            Allowed values for this property are: "emailVerification", "passwordReset", "createUser", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        """
        self.swagger_types = {
            'expires_after': 'int',
            'type': 'str'
        }
        self.attribute_map = {
            'expires_after': 'expiresAfter',
            'type': 'type'
        }
        self._expires_after = None
        self._type = None

    @property
    def expires_after(self):
        """
        Gets the expires_after of this IdentitySettingsTokens.
        Indicates the number of minutes after which the token expires automatically.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The expires_after of this IdentitySettingsTokens.
        :rtype: int
        """
        return self._expires_after

    @expires_after.setter
    def expires_after(self, expires_after):
        """
        Sets the expires_after of this IdentitySettingsTokens.
        Indicates the number of minutes after which the token expires automatically.

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param expires_after: The expires_after of this IdentitySettingsTokens.
        :type: int
        """
        self._expires_after = expires_after

    @property
    def type(self):
        """
        **[Required]** Gets the type of this IdentitySettingsTokens.
        The token type.

        **SCIM++ Properties:**
         - caseExact: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "emailVerification", "passwordReset", "createUser", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this IdentitySettingsTokens.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this IdentitySettingsTokens.
        The token type.

        **SCIM++ Properties:**
         - caseExact: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param type: The type of this IdentitySettingsTokens.
        :type: str
        """
        allowed_values = ["emailVerification", "passwordReset", "createUser"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
