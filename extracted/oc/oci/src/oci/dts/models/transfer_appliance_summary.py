# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 1.0.017


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TransferApplianceSummary(object):
    """
    TransferApplianceSummary model.
    """

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "REQUESTED"
    LIFECYCLE_STATE_REQUESTED = "REQUESTED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "ORACLE_PREPARING"
    LIFECYCLE_STATE_ORACLE_PREPARING = "ORACLE_PREPARING"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "SHIPPING"
    LIFECYCLE_STATE_SHIPPING = "SHIPPING"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "DELIVERED"
    LIFECYCLE_STATE_DELIVERED = "DELIVERED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "PREPARING"
    LIFECYCLE_STATE_PREPARING = "PREPARING"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "FINALIZED"
    LIFECYCLE_STATE_FINALIZED = "FINALIZED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "RETURN_LABEL_REQUESTED"
    LIFECYCLE_STATE_RETURN_LABEL_REQUESTED = "RETURN_LABEL_REQUESTED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "RETURN_LABEL_GENERATING"
    LIFECYCLE_STATE_RETURN_LABEL_GENERATING = "RETURN_LABEL_GENERATING"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "RETURN_LABEL_AVAILABLE"
    LIFECYCLE_STATE_RETURN_LABEL_AVAILABLE = "RETURN_LABEL_AVAILABLE"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "RETURN_DELAYED"
    LIFECYCLE_STATE_RETURN_DELAYED = "RETURN_DELAYED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "RETURN_SHIPPED"
    LIFECYCLE_STATE_RETURN_SHIPPED = "RETURN_SHIPPED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "RETURN_SHIPPED_CANCELLED"
    LIFECYCLE_STATE_RETURN_SHIPPED_CANCELLED = "RETURN_SHIPPED_CANCELLED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "ORACLE_RECEIVED"
    LIFECYCLE_STATE_ORACLE_RECEIVED = "ORACLE_RECEIVED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "ORACLE_RECEIVED_CANCELLED"
    LIFECYCLE_STATE_ORACLE_RECEIVED_CANCELLED = "ORACLE_RECEIVED_CANCELLED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "PROCESSING"
    LIFECYCLE_STATE_PROCESSING = "PROCESSING"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "COMPLETE"
    LIFECYCLE_STATE_COMPLETE = "COMPLETE"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "CUSTOMER_NEVER_RECEIVED"
    LIFECYCLE_STATE_CUSTOMER_NEVER_RECEIVED = "CUSTOMER_NEVER_RECEIVED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "ORACLE_NEVER_RECEIVED"
    LIFECYCLE_STATE_ORACLE_NEVER_RECEIVED = "ORACLE_NEVER_RECEIVED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "CUSTOMER_LOST"
    LIFECYCLE_STATE_CUSTOMER_LOST = "CUSTOMER_LOST"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "CANCELLED"
    LIFECYCLE_STATE_CANCELLED = "CANCELLED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "REJECTED"
    LIFECYCLE_STATE_REJECTED = "REJECTED"

    #: A constant which can be used with the lifecycle_state property of a TransferApplianceSummary.
    #: This constant has a value of "ERROR"
    LIFECYCLE_STATE_ERROR = "ERROR"

    def __init__(self, **kwargs):
        """
        Initializes a new TransferApplianceSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param label:
            The value to assign to the label property of this TransferApplianceSummary.
        :type label: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this TransferApplianceSummary.
            Allowed values for this property are: "REQUESTED", "ORACLE_PREPARING", "SHIPPING", "DELIVERED", "PREPARING", "FINALIZED", "RETURN_LABEL_REQUESTED", "RETURN_LABEL_GENERATING", "RETURN_LABEL_AVAILABLE", "RETURN_DELAYED", "RETURN_SHIPPED", "RETURN_SHIPPED_CANCELLED", "ORACLE_RECEIVED", "ORACLE_RECEIVED_CANCELLED", "PROCESSING", "COMPLETE", "CUSTOMER_NEVER_RECEIVED", "ORACLE_NEVER_RECEIVED", "CUSTOMER_LOST", "CANCELLED", "DELETED", "REJECTED", "ERROR", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param serial_number:
            The value to assign to the serial_number property of this TransferApplianceSummary.
        :type serial_number: str

        :param creation_time:
            The value to assign to the creation_time property of this TransferApplianceSummary.
        :type creation_time: datetime

        """
        self.swagger_types = {
            'label': 'str',
            'lifecycle_state': 'str',
            'serial_number': 'str',
            'creation_time': 'datetime'
        }
        self.attribute_map = {
            'label': 'label',
            'lifecycle_state': 'lifecycleState',
            'serial_number': 'serialNumber',
            'creation_time': 'creationTime'
        }
        self._label = None
        self._lifecycle_state = None
        self._serial_number = None
        self._creation_time = None

    @property
    def label(self):
        """
        Gets the label of this TransferApplianceSummary.

        :return: The label of this TransferApplianceSummary.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """
        Sets the label of this TransferApplianceSummary.

        :param label: The label of this TransferApplianceSummary.
        :type: str
        """
        self._label = label

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this TransferApplianceSummary.
        Allowed values for this property are: "REQUESTED", "ORACLE_PREPARING", "SHIPPING", "DELIVERED", "PREPARING", "FINALIZED", "RETURN_LABEL_REQUESTED", "RETURN_LABEL_GENERATING", "RETURN_LABEL_AVAILABLE", "RETURN_DELAYED", "RETURN_SHIPPED", "RETURN_SHIPPED_CANCELLED", "ORACLE_RECEIVED", "ORACLE_RECEIVED_CANCELLED", "PROCESSING", "COMPLETE", "CUSTOMER_NEVER_RECEIVED", "ORACLE_NEVER_RECEIVED", "CUSTOMER_LOST", "CANCELLED", "DELETED", "REJECTED", "ERROR", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this TransferApplianceSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this TransferApplianceSummary.

        :param lifecycle_state: The lifecycle_state of this TransferApplianceSummary.
        :type: str
        """
        allowed_values = ["REQUESTED", "ORACLE_PREPARING", "SHIPPING", "DELIVERED", "PREPARING", "FINALIZED", "RETURN_LABEL_REQUESTED", "RETURN_LABEL_GENERATING", "RETURN_LABEL_AVAILABLE", "RETURN_DELAYED", "RETURN_SHIPPED", "RETURN_SHIPPED_CANCELLED", "ORACLE_RECEIVED", "ORACLE_RECEIVED_CANCELLED", "PROCESSING", "COMPLETE", "CUSTOMER_NEVER_RECEIVED", "ORACLE_NEVER_RECEIVED", "CUSTOMER_LOST", "CANCELLED", "DELETED", "REJECTED", "ERROR"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def serial_number(self):
        """
        Gets the serial_number of this TransferApplianceSummary.

        :return: The serial_number of this TransferApplianceSummary.
        :rtype: str
        """
        return self._serial_number

    @serial_number.setter
    def serial_number(self, serial_number):
        """
        Sets the serial_number of this TransferApplianceSummary.

        :param serial_number: The serial_number of this TransferApplianceSummary.
        :type: str
        """
        self._serial_number = serial_number

    @property
    def creation_time(self):
        """
        Gets the creation_time of this TransferApplianceSummary.

        :return: The creation_time of this TransferApplianceSummary.
        :rtype: datetime
        """
        return self._creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        """
        Sets the creation_time of this TransferApplianceSummary.

        :param creation_time: The creation_time of this TransferApplianceSummary.
        :type: datetime
        """
        self._creation_time = creation_time

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
