# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220915


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class BackupCopyStatusDetails(object):
    """
    Backup Copy Status details
    """

    #: A constant which can be used with the state property of a BackupCopyStatusDetails.
    #: This constant has a value of "NOT_STARTED"
    STATE_NOT_STARTED = "NOT_STARTED"

    #: A constant which can be used with the state property of a BackupCopyStatusDetails.
    #: This constant has a value of "COPYING"
    STATE_COPYING = "COPYING"

    #: A constant which can be used with the state property of a BackupCopyStatusDetails.
    #: This constant has a value of "COPIED"
    STATE_COPIED = "COPIED"

    #: A constant which can be used with the state property of a BackupCopyStatusDetails.
    #: This constant has a value of "FAILED"
    STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new BackupCopyStatusDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param state:
            The value to assign to the state property of this BackupCopyStatusDetails.
            Allowed values for this property are: "NOT_STARTED", "COPYING", "COPIED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type state: str

        :param state_details:
            The value to assign to the state_details property of this BackupCopyStatusDetails.
        :type state_details: str

        :param backup_id:
            The value to assign to the backup_id property of this BackupCopyStatusDetails.
        :type backup_id: str

        :param region:
            The value to assign to the region property of this BackupCopyStatusDetails.
        :type region: str

        """
        self.swagger_types = {
            'state': 'str',
            'state_details': 'str',
            'backup_id': 'str',
            'region': 'str'
        }
        self.attribute_map = {
            'state': 'state',
            'state_details': 'stateDetails',
            'backup_id': 'backupId',
            'region': 'region'
        }
        self._state = None
        self._state_details = None
        self._backup_id = None
        self._region = None

    @property
    def state(self):
        """
        Gets the state of this BackupCopyStatusDetails.
        Copy States

        Allowed values for this property are: "NOT_STARTED", "COPYING", "COPIED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The state of this BackupCopyStatusDetails.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this BackupCopyStatusDetails.
        Copy States


        :param state: The state of this BackupCopyStatusDetails.
        :type: str
        """
        allowed_values = ["NOT_STARTED", "COPYING", "COPIED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(state, allowed_values):
            state = 'UNKNOWN_ENUM_VALUE'
        self._state = state

    @property
    def state_details(self):
        """
        Gets the state_details of this BackupCopyStatusDetails.
        A message describing the current state of copy in more detail


        :return: The state_details of this BackupCopyStatusDetails.
        :rtype: str
        """
        return self._state_details

    @state_details.setter
    def state_details(self, state_details):
        """
        Sets the state_details of this BackupCopyStatusDetails.
        A message describing the current state of copy in more detail


        :param state_details: The state_details of this BackupCopyStatusDetails.
        :type: str
        """
        self._state_details = state_details

    @property
    def backup_id(self):
        """
        Gets the backup_id of this BackupCopyStatusDetails.
        The `OCID`__ of the backup in the source region

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The backup_id of this BackupCopyStatusDetails.
        :rtype: str
        """
        return self._backup_id

    @backup_id.setter
    def backup_id(self, backup_id):
        """
        Sets the backup_id of this BackupCopyStatusDetails.
        The `OCID`__ of the backup in the source region

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param backup_id: The backup_id of this BackupCopyStatusDetails.
        :type: str
        """
        self._backup_id = backup_id

    @property
    def region(self):
        """
        **[Required]** Gets the region of this BackupCopyStatusDetails.
        Region name of the remote region


        :return: The region of this BackupCopyStatusDetails.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """
        Sets the region of this BackupCopyStatusDetails.
        Region name of the remote region


        :param region: The region of this BackupCopyStatusDetails.
        :type: str
        """
        self._region = region

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
