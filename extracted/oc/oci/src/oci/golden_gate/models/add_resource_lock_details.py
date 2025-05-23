# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200407


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddResourceLockDetails(object):
    """
    Used to add a resource lock.
    Resource locks are used to prevent certain APIs from being called for the resource.
    A full lock prevents both updating the resource and deleting the resource. A delete
    lock prevents deleting the resource.
    """

    #: A constant which can be used with the type property of a AddResourceLockDetails.
    #: This constant has a value of "FULL"
    TYPE_FULL = "FULL"

    #: A constant which can be used with the type property of a AddResourceLockDetails.
    #: This constant has a value of "DELETE"
    TYPE_DELETE = "DELETE"

    def __init__(self, **kwargs):
        """
        Initializes a new AddResourceLockDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this AddResourceLockDetails.
            Allowed values for this property are: "FULL", "DELETE"
        :type type: str

        :param message:
            The value to assign to the message property of this AddResourceLockDetails.
        :type message: str

        """
        self.swagger_types = {
            'type': 'str',
            'message': 'str'
        }
        self.attribute_map = {
            'type': 'type',
            'message': 'message'
        }
        self._type = None
        self._message = None

    @property
    def type(self):
        """
        **[Required]** Gets the type of this AddResourceLockDetails.
        Type of the lock.

        Allowed values for this property are: "FULL", "DELETE"


        :return: The type of this AddResourceLockDetails.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this AddResourceLockDetails.
        Type of the lock.


        :param type: The type of this AddResourceLockDetails.
        :type: str
        """
        allowed_values = ["FULL", "DELETE"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            raise ValueError(
                f"Invalid value for `type`, must be None or one of {allowed_values}"
            )
        self._type = type

    @property
    def message(self):
        """
        Gets the message of this AddResourceLockDetails.
        A message added by the creator of the lock. This is typically used to give an
        indication of why the resource is locked.


        :return: The message of this AddResourceLockDetails.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this AddResourceLockDetails.
        A message added by the creator of the lock. This is typically used to give an
        indication of why the resource is locked.


        :param message: The message of this AddResourceLockDetails.
        :type: str
        """
        self._message = message

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
