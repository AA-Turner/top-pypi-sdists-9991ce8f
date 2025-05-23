# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20210216


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ScheduleProtectedDatabaseDeletionDetails(object):
    """
    The details for scheduling deletion of the protected database
    """

    #: A constant which can be used with the deletion_schedule property of a ScheduleProtectedDatabaseDeletionDetails.
    #: This constant has a value of "DELETE_AFTER_RETENTION_PERIOD"
    DELETION_SCHEDULE_DELETE_AFTER_RETENTION_PERIOD = "DELETE_AFTER_RETENTION_PERIOD"

    #: A constant which can be used with the deletion_schedule property of a ScheduleProtectedDatabaseDeletionDetails.
    #: This constant has a value of "DELETE_AFTER_72_HOURS"
    DELETION_SCHEDULE_DELETE_AFTER_72_HOURS = "DELETE_AFTER_72_HOURS"

    def __init__(self, **kwargs):
        """
        Initializes a new ScheduleProtectedDatabaseDeletionDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param deletion_schedule:
            The value to assign to the deletion_schedule property of this ScheduleProtectedDatabaseDeletionDetails.
            Allowed values for this property are: "DELETE_AFTER_RETENTION_PERIOD", "DELETE_AFTER_72_HOURS"
        :type deletion_schedule: str

        """
        self.swagger_types = {
            'deletion_schedule': 'str'
        }
        self.attribute_map = {
            'deletion_schedule': 'deletionSchedule'
        }
        self._deletion_schedule = None

    @property
    def deletion_schedule(self):
        """
        Gets the deletion_schedule of this ScheduleProtectedDatabaseDeletionDetails.
        Defines a preferred schedule to delete a protected database after you terminate the source database.
        * The default schedule is DELETE_AFTER_72_HOURS, so that the delete operation can occur 72 hours (3 days) after the source database is terminated.
        * The alternate schedule is DELETE_AFTER_RETENTION_PERIOD. Specify this option if you want to delete a protected database only after the policy-defined backup retention period expires.

        Allowed values for this property are: "DELETE_AFTER_RETENTION_PERIOD", "DELETE_AFTER_72_HOURS"


        :return: The deletion_schedule of this ScheduleProtectedDatabaseDeletionDetails.
        :rtype: str
        """
        return self._deletion_schedule

    @deletion_schedule.setter
    def deletion_schedule(self, deletion_schedule):
        """
        Sets the deletion_schedule of this ScheduleProtectedDatabaseDeletionDetails.
        Defines a preferred schedule to delete a protected database after you terminate the source database.
        * The default schedule is DELETE_AFTER_72_HOURS, so that the delete operation can occur 72 hours (3 days) after the source database is terminated.
        * The alternate schedule is DELETE_AFTER_RETENTION_PERIOD. Specify this option if you want to delete a protected database only after the policy-defined backup retention period expires.


        :param deletion_schedule: The deletion_schedule of this ScheduleProtectedDatabaseDeletionDetails.
        :type: str
        """
        allowed_values = ["DELETE_AFTER_RETENTION_PERIOD", "DELETE_AFTER_72_HOURS"]
        if not value_allowed_none_or_none_sentinel(deletion_schedule, allowed_values):
            raise ValueError(
                f"Invalid value for `deletion_schedule`, must be None or one of {allowed_values}"
            )
        self._deletion_schedule = deletion_schedule

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
