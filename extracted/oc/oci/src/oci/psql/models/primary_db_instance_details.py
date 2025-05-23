# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220915


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PrimaryDbInstanceDetails(object):
    """
    The primary database instance node details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PrimaryDbInstanceDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param db_instance_id:
            The value to assign to the db_instance_id property of this PrimaryDbInstanceDetails.
        :type db_instance_id: str

        """
        self.swagger_types = {
            'db_instance_id': 'str'
        }
        self.attribute_map = {
            'db_instance_id': 'dbInstanceId'
        }
        self._db_instance_id = None

    @property
    def db_instance_id(self):
        """
        **[Required]** Gets the db_instance_id of this PrimaryDbInstanceDetails.
        A unique identifier for the primary database instance node.


        :return: The db_instance_id of this PrimaryDbInstanceDetails.
        :rtype: str
        """
        return self._db_instance_id

    @db_instance_id.setter
    def db_instance_id(self, db_instance_id):
        """
        Sets the db_instance_id of this PrimaryDbInstanceDetails.
        A unique identifier for the primary database instance node.


        :param db_instance_id: The db_instance_id of this PrimaryDbInstanceDetails.
        :type: str
        """
        self._db_instance_id = db_instance_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
