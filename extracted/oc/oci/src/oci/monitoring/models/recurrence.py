# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20180401

from .suppression_condition import SuppressionCondition
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Recurrence(SuppressionCondition):
    """
    Alarm suppression recurring schedule. Only one recurrence condition is supported within the list of preconditions for a suppression (`suppressionConditions`).
    """

    def __init__(self, **kwargs):
        """
        Initializes a new Recurrence object with values from keyword arguments. The default value of the :py:attr:`~oci.monitoring.models.Recurrence.condition_type` attribute
        of this class is ``RECURRENCE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param condition_type:
            The value to assign to the condition_type property of this Recurrence.
            Allowed values for this property are: "RECURRENCE"
        :type condition_type: str

        :param suppression_recurrence:
            The value to assign to the suppression_recurrence property of this Recurrence.
        :type suppression_recurrence: str

        :param suppression_duration:
            The value to assign to the suppression_duration property of this Recurrence.
        :type suppression_duration: str

        """
        self.swagger_types = {
            'condition_type': 'str',
            'suppression_recurrence': 'str',
            'suppression_duration': 'str'
        }
        self.attribute_map = {
            'condition_type': 'conditionType',
            'suppression_recurrence': 'suppressionRecurrence',
            'suppression_duration': 'suppressionDuration'
        }
        self._condition_type = None
        self._suppression_recurrence = None
        self._suppression_duration = None
        self._condition_type = 'RECURRENCE'

    @property
    def suppression_recurrence(self):
        """
        **[Required]** Gets the suppression_recurrence of this Recurrence.
        Frequency and start time of the recurring suppression. The format follows
        `the iCalendar specification (RFC 5545, section 3.3.10)`__.
        Supported rule parts:
        * `FREQ`: Frequency of the recurring suppression: `WEEKLY` or `DAILY` only.
        * `BYDAY`: Comma separated days. Use with weekly suppressions only. Supported values: `MO`, `TU`, `WE`, `TH`, `FR`, `SA` ,`SU`.
        * `BYHOUR`, `BYMINUTE`, `BYSECOND`: Start time in UTC, after `timeSuppressFrom` value. Default is 00:00:00 UTC after `timeSuppressFrom`.

        __ https://datatracker.ietf.org/doc/html/rfc5545#section-3.3.10


        :return: The suppression_recurrence of this Recurrence.
        :rtype: str
        """
        return self._suppression_recurrence

    @suppression_recurrence.setter
    def suppression_recurrence(self, suppression_recurrence):
        """
        Sets the suppression_recurrence of this Recurrence.
        Frequency and start time of the recurring suppression. The format follows
        `the iCalendar specification (RFC 5545, section 3.3.10)`__.
        Supported rule parts:
        * `FREQ`: Frequency of the recurring suppression: `WEEKLY` or `DAILY` only.
        * `BYDAY`: Comma separated days. Use with weekly suppressions only. Supported values: `MO`, `TU`, `WE`, `TH`, `FR`, `SA` ,`SU`.
        * `BYHOUR`, `BYMINUTE`, `BYSECOND`: Start time in UTC, after `timeSuppressFrom` value. Default is 00:00:00 UTC after `timeSuppressFrom`.

        __ https://datatracker.ietf.org/doc/html/rfc5545#section-3.3.10


        :param suppression_recurrence: The suppression_recurrence of this Recurrence.
        :type: str
        """
        self._suppression_recurrence = suppression_recurrence

    @property
    def suppression_duration(self):
        """
        **[Required]** Gets the suppression_duration of this Recurrence.
        Duration of the recurring suppression. Specified as a string in ISO 8601 format. Minimum: `PT1M` (1 minute). Maximum: `PT24H` (24 hours).


        :return: The suppression_duration of this Recurrence.
        :rtype: str
        """
        return self._suppression_duration

    @suppression_duration.setter
    def suppression_duration(self, suppression_duration):
        """
        Sets the suppression_duration of this Recurrence.
        Duration of the recurring suppression. Specified as a string in ISO 8601 format. Minimum: `PT1M` (1 minute). Maximum: `PT24H` (24 hours).


        :param suppression_duration: The suppression_duration of this Recurrence.
        :type: str
        """
        self._suppression_duration = suppression_duration

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
