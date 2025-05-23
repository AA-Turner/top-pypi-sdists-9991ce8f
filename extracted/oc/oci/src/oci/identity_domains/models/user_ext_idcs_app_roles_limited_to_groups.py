# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: v1


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UserExtIdcsAppRolesLimitedToGroups(object):
    """
    Description:

    **Added In:** 19.2.1

    **SCIM++ Properties:**
    - idcsCompositeKey: [value, idcsAppRoleId]
    - idcsSearchable: true
    - multiValued: true
    - mutability: readOnly
    - required: false
    - returned: request
    - type: complex
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UserExtIdcsAppRolesLimitedToGroups object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param idcs_app_role_id:
            The value to assign to the idcs_app_role_id property of this UserExtIdcsAppRolesLimitedToGroups.
        :type idcs_app_role_id: str

        :param value:
            The value to assign to the value property of this UserExtIdcsAppRolesLimitedToGroups.
        :type value: str

        :param ref:
            The value to assign to the ref property of this UserExtIdcsAppRolesLimitedToGroups.
        :type ref: str

        :param display:
            The value to assign to the display property of this UserExtIdcsAppRolesLimitedToGroups.
        :type display: str

        :param ocid:
            The value to assign to the ocid property of this UserExtIdcsAppRolesLimitedToGroups.
        :type ocid: str

        """
        self.swagger_types = {
            'idcs_app_role_id': 'str',
            'value': 'str',
            'ref': 'str',
            'display': 'str',
            'ocid': 'str'
        }
        self.attribute_map = {
            'idcs_app_role_id': 'idcsAppRoleId',
            'value': 'value',
            'ref': '$ref',
            'display': 'display',
            'ocid': 'ocid'
        }
        self._idcs_app_role_id = None
        self._value = None
        self._ref = None
        self._display = None
        self._ocid = None

    @property
    def idcs_app_role_id(self):
        """
        **[Required]** Gets the idcs_app_role_id of this UserExtIdcsAppRolesLimitedToGroups.
        The id of the Oracle Identity Cloud Service AppRole grant limited to one or more Groups.

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsCsvAttributeName: IDCS AppRole Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The idcs_app_role_id of this UserExtIdcsAppRolesLimitedToGroups.
        :rtype: str
        """
        return self._idcs_app_role_id

    @idcs_app_role_id.setter
    def idcs_app_role_id(self, idcs_app_role_id):
        """
        Sets the idcs_app_role_id of this UserExtIdcsAppRolesLimitedToGroups.
        The id of the Oracle Identity Cloud Service AppRole grant limited to one or more Groups.

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsCsvAttributeName: IDCS AppRole Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param idcs_app_role_id: The idcs_app_role_id of this UserExtIdcsAppRolesLimitedToGroups.
        :type: str
        """
        self._idcs_app_role_id = idcs_app_role_id

    @property
    def value(self):
        """
        **[Required]** Gets the value of this UserExtIdcsAppRolesLimitedToGroups.
        The id of a Group the AppRole Grant is limited to

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Group Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this UserExtIdcsAppRolesLimitedToGroups.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this UserExtIdcsAppRolesLimitedToGroups.
        The id of a Group the AppRole Grant is limited to

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Group Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this UserExtIdcsAppRolesLimitedToGroups.
        :type: str
        """
        self._value = value

    @property
    def ref(self):
        """
        Gets the ref of this UserExtIdcsAppRolesLimitedToGroups.
        The URI of the SCIM resource representing the Group manager.  RECOMMENDED.

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The ref of this UserExtIdcsAppRolesLimitedToGroups.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this UserExtIdcsAppRolesLimitedToGroups.
        The URI of the SCIM resource representing the Group manager.  RECOMMENDED.

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param ref: The ref of this UserExtIdcsAppRolesLimitedToGroups.
        :type: str
        """
        self._ref = ref

    @property
    def display(self):
        """
        Gets the display of this UserExtIdcsAppRolesLimitedToGroups.
        Group display name

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The display of this UserExtIdcsAppRolesLimitedToGroups.
        :rtype: str
        """
        return self._display

    @display.setter
    def display(self, display):
        """
        Sets the display of this UserExtIdcsAppRolesLimitedToGroups.
        Group display name

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param display: The display of this UserExtIdcsAppRolesLimitedToGroups.
        :type: str
        """
        self._display = display

    @property
    def ocid(self):
        """
        Gets the ocid of this UserExtIdcsAppRolesLimitedToGroups.
        The ocid of a Group the AppRole Grant is limited to

        **Added In:** 2202230830

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Group Ocid
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The ocid of this UserExtIdcsAppRolesLimitedToGroups.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this UserExtIdcsAppRolesLimitedToGroups.
        The ocid of a Group the AppRole Grant is limited to

        **Added In:** 2202230830

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Group Ocid
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param ocid: The ocid of this UserExtIdcsAppRolesLimitedToGroups.
        :type: str
        """
        self._ocid = ocid

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
