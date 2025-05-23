# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200601


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Dependency(object):
    """
    Details of a dependency an object or feature defines on another. For
    example, a source may depend on a parser either directly or indirectly.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new Dependency object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this Dependency.
        :type type: str

        :param reference_type:
            The value to assign to the reference_type property of this Dependency.
        :type reference_type: str

        :param reference_id:
            The value to assign to the reference_id property of this Dependency.
        :type reference_id: int

        :param reference_name:
            The value to assign to the reference_name property of this Dependency.
        :type reference_name: str

        :param reference_display_name:
            The value to assign to the reference_display_name property of this Dependency.
        :type reference_display_name: str

        """
        self.swagger_types = {
            'type': 'str',
            'reference_type': 'str',
            'reference_id': 'int',
            'reference_name': 'str',
            'reference_display_name': 'str'
        }
        self.attribute_map = {
            'type': 'type',
            'reference_type': 'referenceType',
            'reference_id': 'referenceId',
            'reference_name': 'referenceName',
            'reference_display_name': 'referenceDisplayName'
        }
        self._type = None
        self._reference_type = None
        self._reference_id = None
        self._reference_name = None
        self._reference_display_name = None

    @property
    def type(self):
        """
        Gets the type of this Dependency.
        The dependency type.


        :return: The type of this Dependency.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this Dependency.
        The dependency type.


        :param type: The type of this Dependency.
        :type: str
        """
        self._type = type

    @property
    def reference_type(self):
        """
        Gets the reference_type of this Dependency.
        The type of reference that defines the dependency.


        :return: The reference_type of this Dependency.
        :rtype: str
        """
        return self._reference_type

    @reference_type.setter
    def reference_type(self, reference_type):
        """
        Sets the reference_type of this Dependency.
        The type of reference that defines the dependency.


        :param reference_type: The reference_type of this Dependency.
        :type: str
        """
        self._reference_type = reference_type

    @property
    def reference_id(self):
        """
        Gets the reference_id of this Dependency.
        The unique identifier of the reference, if available.


        :return: The reference_id of this Dependency.
        :rtype: int
        """
        return self._reference_id

    @reference_id.setter
    def reference_id(self, reference_id):
        """
        Sets the reference_id of this Dependency.
        The unique identifier of the reference, if available.


        :param reference_id: The reference_id of this Dependency.
        :type: int
        """
        self._reference_id = reference_id

    @property
    def reference_name(self):
        """
        Gets the reference_name of this Dependency.
        The name of the dependency object


        :return: The reference_name of this Dependency.
        :rtype: str
        """
        return self._reference_name

    @reference_name.setter
    def reference_name(self, reference_name):
        """
        Sets the reference_name of this Dependency.
        The name of the dependency object


        :param reference_name: The reference_name of this Dependency.
        :type: str
        """
        self._reference_name = reference_name

    @property
    def reference_display_name(self):
        """
        Gets the reference_display_name of this Dependency.
        The display name of the dependency object


        :return: The reference_display_name of this Dependency.
        :rtype: str
        """
        return self._reference_display_name

    @reference_display_name.setter
    def reference_display_name(self, reference_display_name):
        """
        Sets the reference_display_name of this Dependency.
        The display name of the dependency object


        :param reference_display_name: The reference_display_name of this Dependency.
        :type: str
        """
        self._reference_display_name = reference_display_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
