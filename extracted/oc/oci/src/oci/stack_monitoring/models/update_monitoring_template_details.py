# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20210330


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateMonitoringTemplateDetails(object):
    """
    The information about updating a monitoring template. The monitoring template displayName should be unique in a compartment.
    """

    #: A constant which can be used with the message_format property of a UpdateMonitoringTemplateDetails.
    #: This constant has a value of "RAW"
    MESSAGE_FORMAT_RAW = "RAW"

    #: A constant which can be used with the message_format property of a UpdateMonitoringTemplateDetails.
    #: This constant has a value of "PRETTY_JSON"
    MESSAGE_FORMAT_PRETTY_JSON = "PRETTY_JSON"

    #: A constant which can be used with the message_format property of a UpdateMonitoringTemplateDetails.
    #: This constant has a value of "ONS_OPTIMIZED"
    MESSAGE_FORMAT_ONS_OPTIMIZED = "ONS_OPTIMIZED"

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateMonitoringTemplateDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdateMonitoringTemplateDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this UpdateMonitoringTemplateDetails.
        :type description: str

        :param destinations:
            The value to assign to the destinations property of this UpdateMonitoringTemplateDetails.
        :type destinations: list[str]

        :param is_alarms_enabled:
            The value to assign to the is_alarms_enabled property of this UpdateMonitoringTemplateDetails.
        :type is_alarms_enabled: bool

        :param is_split_notification_enabled:
            The value to assign to the is_split_notification_enabled property of this UpdateMonitoringTemplateDetails.
        :type is_split_notification_enabled: bool

        :param members:
            The value to assign to the members property of this UpdateMonitoringTemplateDetails.
        :type members: list[oci.stack_monitoring.models.MemberReference]

        :param repeat_notification_duration:
            The value to assign to the repeat_notification_duration property of this UpdateMonitoringTemplateDetails.
        :type repeat_notification_duration: str

        :param message_format:
            The value to assign to the message_format property of this UpdateMonitoringTemplateDetails.
            Allowed values for this property are: "RAW", "PRETTY_JSON", "ONS_OPTIMIZED"
        :type message_format: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateMonitoringTemplateDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateMonitoringTemplateDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'description': 'str',
            'destinations': 'list[str]',
            'is_alarms_enabled': 'bool',
            'is_split_notification_enabled': 'bool',
            'members': 'list[MemberReference]',
            'repeat_notification_duration': 'str',
            'message_format': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }
        self.attribute_map = {
            'display_name': 'displayName',
            'description': 'description',
            'destinations': 'destinations',
            'is_alarms_enabled': 'isAlarmsEnabled',
            'is_split_notification_enabled': 'isSplitNotificationEnabled',
            'members': 'members',
            'repeat_notification_duration': 'repeatNotificationDuration',
            'message_format': 'messageFormat',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }
        self._display_name = None
        self._description = None
        self._destinations = None
        self._is_alarms_enabled = None
        self._is_split_notification_enabled = None
        self._members = None
        self._repeat_notification_duration = None
        self._message_format = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateMonitoringTemplateDetails.
        A user-friendly name for the monitoring template. It is unique and mutable in nature.


        :return: The display_name of this UpdateMonitoringTemplateDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateMonitoringTemplateDetails.
        A user-friendly name for the monitoring template. It is unique and mutable in nature.


        :param display_name: The display_name of this UpdateMonitoringTemplateDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this UpdateMonitoringTemplateDetails.
        A user-friendly description for the monitoring template. It does not have to be unique, and it's changeable.


        :return: The description of this UpdateMonitoringTemplateDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateMonitoringTemplateDetails.
        A user-friendly description for the monitoring template. It does not have to be unique, and it's changeable.


        :param description: The description of this UpdateMonitoringTemplateDetails.
        :type: str
        """
        self._description = description

    @property
    def destinations(self):
        """
        Gets the destinations of this UpdateMonitoringTemplateDetails.
        A list of destinations for alarm notifications. Each destination is represented by the OCID of a related resource


        :return: The destinations of this UpdateMonitoringTemplateDetails.
        :rtype: list[str]
        """
        return self._destinations

    @destinations.setter
    def destinations(self, destinations):
        """
        Sets the destinations of this UpdateMonitoringTemplateDetails.
        A list of destinations for alarm notifications. Each destination is represented by the OCID of a related resource


        :param destinations: The destinations of this UpdateMonitoringTemplateDetails.
        :type: list[str]
        """
        self._destinations = destinations

    @property
    def is_alarms_enabled(self):
        """
        Gets the is_alarms_enabled of this UpdateMonitoringTemplateDetails.
        User can create the out of box alarm only for multiple resourceTypes not for individual resource instances and groups for specified compartment.


        :return: The is_alarms_enabled of this UpdateMonitoringTemplateDetails.
        :rtype: bool
        """
        return self._is_alarms_enabled

    @is_alarms_enabled.setter
    def is_alarms_enabled(self, is_alarms_enabled):
        """
        Sets the is_alarms_enabled of this UpdateMonitoringTemplateDetails.
        User can create the out of box alarm only for multiple resourceTypes not for individual resource instances and groups for specified compartment.


        :param is_alarms_enabled: The is_alarms_enabled of this UpdateMonitoringTemplateDetails.
        :type: bool
        """
        self._is_alarms_enabled = is_alarms_enabled

    @property
    def is_split_notification_enabled(self):
        """
        Gets the is_split_notification_enabled of this UpdateMonitoringTemplateDetails.
        Whether the alarm notification is enabled or disabled, it will be Enabled by default.


        :return: The is_split_notification_enabled of this UpdateMonitoringTemplateDetails.
        :rtype: bool
        """
        return self._is_split_notification_enabled

    @is_split_notification_enabled.setter
    def is_split_notification_enabled(self, is_split_notification_enabled):
        """
        Sets the is_split_notification_enabled of this UpdateMonitoringTemplateDetails.
        Whether the alarm notification is enabled or disabled, it will be Enabled by default.


        :param is_split_notification_enabled: The is_split_notification_enabled of this UpdateMonitoringTemplateDetails.
        :type: bool
        """
        self._is_split_notification_enabled = is_split_notification_enabled

    @property
    def members(self):
        """
        Gets the members of this UpdateMonitoringTemplateDetails.
        List of members of this monitoring template.


        :return: The members of this UpdateMonitoringTemplateDetails.
        :rtype: list[oci.stack_monitoring.models.MemberReference]
        """
        return self._members

    @members.setter
    def members(self, members):
        """
        Sets the members of this UpdateMonitoringTemplateDetails.
        List of members of this monitoring template.


        :param members: The members of this UpdateMonitoringTemplateDetails.
        :type: list[oci.stack_monitoring.models.MemberReference]
        """
        self._members = members

    @property
    def repeat_notification_duration(self):
        """
        Gets the repeat_notification_duration of this UpdateMonitoringTemplateDetails.
        The frequency for re-submitting alarm notifications, if the alarm keeps firing without interruption. Format defined by ISO 8601. For example, PT4H indicates four hours. Minimum- PT1M. Maximum - P30D.


        :return: The repeat_notification_duration of this UpdateMonitoringTemplateDetails.
        :rtype: str
        """
        return self._repeat_notification_duration

    @repeat_notification_duration.setter
    def repeat_notification_duration(self, repeat_notification_duration):
        """
        Sets the repeat_notification_duration of this UpdateMonitoringTemplateDetails.
        The frequency for re-submitting alarm notifications, if the alarm keeps firing without interruption. Format defined by ISO 8601. For example, PT4H indicates four hours. Minimum- PT1M. Maximum - P30D.


        :param repeat_notification_duration: The repeat_notification_duration of this UpdateMonitoringTemplateDetails.
        :type: str
        """
        self._repeat_notification_duration = repeat_notification_duration

    @property
    def message_format(self):
        """
        Gets the message_format of this UpdateMonitoringTemplateDetails.
        The format to use for alarm notifications.

        Allowed values for this property are: "RAW", "PRETTY_JSON", "ONS_OPTIMIZED"


        :return: The message_format of this UpdateMonitoringTemplateDetails.
        :rtype: str
        """
        return self._message_format

    @message_format.setter
    def message_format(self, message_format):
        """
        Sets the message_format of this UpdateMonitoringTemplateDetails.
        The format to use for alarm notifications.


        :param message_format: The message_format of this UpdateMonitoringTemplateDetails.
        :type: str
        """
        allowed_values = ["RAW", "PRETTY_JSON", "ONS_OPTIMIZED"]
        if not value_allowed_none_or_none_sentinel(message_format, allowed_values):
            raise ValueError(
                f"Invalid value for `message_format`, must be None or one of {allowed_values}"
            )
        self._message_format = message_format

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateMonitoringTemplateDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this UpdateMonitoringTemplateDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateMonitoringTemplateDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this UpdateMonitoringTemplateDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateMonitoringTemplateDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this UpdateMonitoringTemplateDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateMonitoringTemplateDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this UpdateMonitoringTemplateDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
