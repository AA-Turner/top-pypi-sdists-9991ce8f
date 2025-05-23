# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20190531


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ResourcePrincipalConfiguration(object):
    """
    Resource Principal Session Token Details.
    """

    #: A constant which can be used with the lifecycle_state property of a ResourcePrincipalConfiguration.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a ResourcePrincipalConfiguration.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ResourcePrincipalConfiguration.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a ResourcePrincipalConfiguration.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a ResourcePrincipalConfiguration.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a ResourcePrincipalConfiguration.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new ResourcePrincipalConfiguration object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ResourcePrincipalConfiguration.
        :type id: str

        :param bds_instance_id:
            The value to assign to the bds_instance_id property of this ResourcePrincipalConfiguration.
        :type bds_instance_id: str

        :param display_name:
            The value to assign to the display_name property of this ResourcePrincipalConfiguration.
        :type display_name: str

        :param session_token_life_span_duration_in_hours:
            The value to assign to the session_token_life_span_duration_in_hours property of this ResourcePrincipalConfiguration.
        :type session_token_life_span_duration_in_hours: int

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ResourcePrincipalConfiguration.
            Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_token_refreshed:
            The value to assign to the time_token_refreshed property of this ResourcePrincipalConfiguration.
        :type time_token_refreshed: datetime

        :param time_token_expiry:
            The value to assign to the time_token_expiry property of this ResourcePrincipalConfiguration.
        :type time_token_expiry: datetime

        :param time_created:
            The value to assign to the time_created property of this ResourcePrincipalConfiguration.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ResourcePrincipalConfiguration.
        :type time_updated: datetime

        """
        self.swagger_types = {
            'id': 'str',
            'bds_instance_id': 'str',
            'display_name': 'str',
            'session_token_life_span_duration_in_hours': 'int',
            'lifecycle_state': 'str',
            'time_token_refreshed': 'datetime',
            'time_token_expiry': 'datetime',
            'time_created': 'datetime',
            'time_updated': 'datetime'
        }
        self.attribute_map = {
            'id': 'id',
            'bds_instance_id': 'bdsInstanceId',
            'display_name': 'displayName',
            'session_token_life_span_duration_in_hours': 'sessionTokenLifeSpanDurationInHours',
            'lifecycle_state': 'lifecycleState',
            'time_token_refreshed': 'timeTokenRefreshed',
            'time_token_expiry': 'timeTokenExpiry',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated'
        }
        self._id = None
        self._bds_instance_id = None
        self._display_name = None
        self._session_token_life_span_duration_in_hours = None
        self._lifecycle_state = None
        self._time_token_refreshed = None
        self._time_token_expiry = None
        self._time_created = None
        self._time_updated = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ResourcePrincipalConfiguration.
        The id of the ResourcePrincipalConfiguration.


        :return: The id of this ResourcePrincipalConfiguration.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ResourcePrincipalConfiguration.
        The id of the ResourcePrincipalConfiguration.


        :param id: The id of this ResourcePrincipalConfiguration.
        :type: str
        """
        self._id = id

    @property
    def bds_instance_id(self):
        """
        **[Required]** Gets the bds_instance_id of this ResourcePrincipalConfiguration.
        The OCID of the bdsInstance which is the parent resource id.


        :return: The bds_instance_id of this ResourcePrincipalConfiguration.
        :rtype: str
        """
        return self._bds_instance_id

    @bds_instance_id.setter
    def bds_instance_id(self, bds_instance_id):
        """
        Sets the bds_instance_id of this ResourcePrincipalConfiguration.
        The OCID of the bdsInstance which is the parent resource id.


        :param bds_instance_id: The bds_instance_id of this ResourcePrincipalConfiguration.
        :type: str
        """
        self._bds_instance_id = bds_instance_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ResourcePrincipalConfiguration.
        A user-friendly name. Only ASCII alphanumeric characters with no spaces allowed. The name does not have to be unique, and it may be changed. Avoid entering confidential information.


        :return: The display_name of this ResourcePrincipalConfiguration.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ResourcePrincipalConfiguration.
        A user-friendly name. Only ASCII alphanumeric characters with no spaces allowed. The name does not have to be unique, and it may be changed. Avoid entering confidential information.


        :param display_name: The display_name of this ResourcePrincipalConfiguration.
        :type: str
        """
        self._display_name = display_name

    @property
    def session_token_life_span_duration_in_hours(self):
        """
        **[Required]** Gets the session_token_life_span_duration_in_hours of this ResourcePrincipalConfiguration.
        Life span in hours of each resource principal session token.


        :return: The session_token_life_span_duration_in_hours of this ResourcePrincipalConfiguration.
        :rtype: int
        """
        return self._session_token_life_span_duration_in_hours

    @session_token_life_span_duration_in_hours.setter
    def session_token_life_span_duration_in_hours(self, session_token_life_span_duration_in_hours):
        """
        Sets the session_token_life_span_duration_in_hours of this ResourcePrincipalConfiguration.
        Life span in hours of each resource principal session token.


        :param session_token_life_span_duration_in_hours: The session_token_life_span_duration_in_hours of this ResourcePrincipalConfiguration.
        :type: int
        """
        self._session_token_life_span_duration_in_hours = session_token_life_span_duration_in_hours

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ResourcePrincipalConfiguration.
        The state of the ResourcePrincipalConfiguration.

        Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ResourcePrincipalConfiguration.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ResourcePrincipalConfiguration.
        The state of the ResourcePrincipalConfiguration.


        :param lifecycle_state: The lifecycle_state of this ResourcePrincipalConfiguration.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def time_token_refreshed(self):
        """
        Gets the time_token_refreshed of this ResourcePrincipalConfiguration.
        the time the resource principal session token was refreshed, shown as an rfc 3339 formatted datetime string.


        :return: The time_token_refreshed of this ResourcePrincipalConfiguration.
        :rtype: datetime
        """
        return self._time_token_refreshed

    @time_token_refreshed.setter
    def time_token_refreshed(self, time_token_refreshed):
        """
        Sets the time_token_refreshed of this ResourcePrincipalConfiguration.
        the time the resource principal session token was refreshed, shown as an rfc 3339 formatted datetime string.


        :param time_token_refreshed: The time_token_refreshed of this ResourcePrincipalConfiguration.
        :type: datetime
        """
        self._time_token_refreshed = time_token_refreshed

    @property
    def time_token_expiry(self):
        """
        Gets the time_token_expiry of this ResourcePrincipalConfiguration.
        the time the resource principal session token will expired, shown as an rfc 3339 formatted datetime string.


        :return: The time_token_expiry of this ResourcePrincipalConfiguration.
        :rtype: datetime
        """
        return self._time_token_expiry

    @time_token_expiry.setter
    def time_token_expiry(self, time_token_expiry):
        """
        Sets the time_token_expiry of this ResourcePrincipalConfiguration.
        the time the resource principal session token will expired, shown as an rfc 3339 formatted datetime string.


        :param time_token_expiry: The time_token_expiry of this ResourcePrincipalConfiguration.
        :type: datetime
        """
        self._time_token_expiry = time_token_expiry

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ResourcePrincipalConfiguration.
        The time the ResourcePrincipalConfiguration was created, shown as an RFC 3339 formatted datetime string.


        :return: The time_created of this ResourcePrincipalConfiguration.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ResourcePrincipalConfiguration.
        The time the ResourcePrincipalConfiguration was created, shown as an RFC 3339 formatted datetime string.


        :param time_created: The time_created of this ResourcePrincipalConfiguration.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        **[Required]** Gets the time_updated of this ResourcePrincipalConfiguration.
        The time the ResourcePrincipalConfiguration was updated, shown as an RFC 3339 formatted datetime string.


        :return: The time_updated of this ResourcePrincipalConfiguration.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ResourcePrincipalConfiguration.
        The time the ResourcePrincipalConfiguration was updated, shown as an RFC 3339 formatted datetime string.


        :param time_updated: The time_updated of this ResourcePrincipalConfiguration.
        :type: datetime
        """
        self._time_updated = time_updated

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
