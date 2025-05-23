# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20160918


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ConvertStandbyAutonomousContainerDatabaseDetails(object):
    """
    The configuration details for change Autonomous Container Database Dataguard role
    """

    #: A constant which can be used with the role property of a ConvertStandbyAutonomousContainerDatabaseDetails.
    #: This constant has a value of "PRIMARY"
    ROLE_PRIMARY = "PRIMARY"

    #: A constant which can be used with the role property of a ConvertStandbyAutonomousContainerDatabaseDetails.
    #: This constant has a value of "STANDBY"
    ROLE_STANDBY = "STANDBY"

    #: A constant which can be used with the role property of a ConvertStandbyAutonomousContainerDatabaseDetails.
    #: This constant has a value of "DISABLED_STANDBY"
    ROLE_DISABLED_STANDBY = "DISABLED_STANDBY"

    #: A constant which can be used with the role property of a ConvertStandbyAutonomousContainerDatabaseDetails.
    #: This constant has a value of "BACKUP_COPY"
    ROLE_BACKUP_COPY = "BACKUP_COPY"

    #: A constant which can be used with the role property of a ConvertStandbyAutonomousContainerDatabaseDetails.
    #: This constant has a value of "SNAPSHOT_STANDBY"
    ROLE_SNAPSHOT_STANDBY = "SNAPSHOT_STANDBY"

    #: A constant which can be used with the connection_strings_type property of a ConvertStandbyAutonomousContainerDatabaseDetails.
    #: This constant has a value of "SNAPSHOT_SERVICES"
    CONNECTION_STRINGS_TYPE_SNAPSHOT_SERVICES = "SNAPSHOT_SERVICES"

    #: A constant which can be used with the connection_strings_type property of a ConvertStandbyAutonomousContainerDatabaseDetails.
    #: This constant has a value of "PRIMARY_SERVICES"
    CONNECTION_STRINGS_TYPE_PRIMARY_SERVICES = "PRIMARY_SERVICES"

    def __init__(self, **kwargs):
        """
        Initializes a new ConvertStandbyAutonomousContainerDatabaseDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param role:
            The value to assign to the role property of this ConvertStandbyAutonomousContainerDatabaseDetails.
            Allowed values for this property are: "PRIMARY", "STANDBY", "DISABLED_STANDBY", "BACKUP_COPY", "SNAPSHOT_STANDBY"
        :type role: str

        :param connection_strings_type:
            The value to assign to the connection_strings_type property of this ConvertStandbyAutonomousContainerDatabaseDetails.
            Allowed values for this property are: "SNAPSHOT_SERVICES", "PRIMARY_SERVICES"
        :type connection_strings_type: str

        """
        self.swagger_types = {
            'role': 'str',
            'connection_strings_type': 'str'
        }
        self.attribute_map = {
            'role': 'role',
            'connection_strings_type': 'connectionStringsType'
        }
        self._role = None
        self._connection_strings_type = None

    @property
    def role(self):
        """
        **[Required]** Gets the role of this ConvertStandbyAutonomousContainerDatabaseDetails.
        The Data Guard role of the Autonomous Container Database or Autonomous Database, if Autonomous Data Guard is enabled.

        Allowed values for this property are: "PRIMARY", "STANDBY", "DISABLED_STANDBY", "BACKUP_COPY", "SNAPSHOT_STANDBY"


        :return: The role of this ConvertStandbyAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """
        Sets the role of this ConvertStandbyAutonomousContainerDatabaseDetails.
        The Data Guard role of the Autonomous Container Database or Autonomous Database, if Autonomous Data Guard is enabled.


        :param role: The role of this ConvertStandbyAutonomousContainerDatabaseDetails.
        :type: str
        """
        allowed_values = ["PRIMARY", "STANDBY", "DISABLED_STANDBY", "BACKUP_COPY", "SNAPSHOT_STANDBY"]
        if not value_allowed_none_or_none_sentinel(role, allowed_values):
            raise ValueError(
                f"Invalid value for `role`, must be None or one of {allowed_values}"
            )
        self._role = role

    @property
    def connection_strings_type(self):
        """
        Gets the connection_strings_type of this ConvertStandbyAutonomousContainerDatabaseDetails.
        type of connection strings when converting database to snapshot mode

        Allowed values for this property are: "SNAPSHOT_SERVICES", "PRIMARY_SERVICES"


        :return: The connection_strings_type of this ConvertStandbyAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._connection_strings_type

    @connection_strings_type.setter
    def connection_strings_type(self, connection_strings_type):
        """
        Sets the connection_strings_type of this ConvertStandbyAutonomousContainerDatabaseDetails.
        type of connection strings when converting database to snapshot mode


        :param connection_strings_type: The connection_strings_type of this ConvertStandbyAutonomousContainerDatabaseDetails.
        :type: str
        """
        allowed_values = ["SNAPSHOT_SERVICES", "PRIMARY_SERVICES"]
        if not value_allowed_none_or_none_sentinel(connection_strings_type, allowed_values):
            raise ValueError(
                f"Invalid value for `connection_strings_type`, must be None or one of {allowed_values}"
            )
        self._connection_strings_type = connection_strings_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
