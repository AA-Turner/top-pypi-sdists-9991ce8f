# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200601


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LogAnalyticsEntityTopologyLink(object):
    """
    Log Analytics entity relationship link used in hierarchical representation of entity relationships topology.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new LogAnalyticsEntityTopologyLink object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source_entity_id:
            The value to assign to the source_entity_id property of this LogAnalyticsEntityTopologyLink.
        :type source_entity_id: str

        :param destination_entity_id:
            The value to assign to the destination_entity_id property of this LogAnalyticsEntityTopologyLink.
        :type destination_entity_id: str

        :param contexts:
            The value to assign to the contexts property of this LogAnalyticsEntityTopologyLink.
        :type contexts: list[str]

        :param time_last_discovered:
            The value to assign to the time_last_discovered property of this LogAnalyticsEntityTopologyLink.
        :type time_last_discovered: datetime

        """
        self.swagger_types = {
            'source_entity_id': 'str',
            'destination_entity_id': 'str',
            'contexts': 'list[str]',
            'time_last_discovered': 'datetime'
        }
        self.attribute_map = {
            'source_entity_id': 'sourceEntityId',
            'destination_entity_id': 'destinationEntityId',
            'contexts': 'contexts',
            'time_last_discovered': 'timeLastDiscovered'
        }
        self._source_entity_id = None
        self._destination_entity_id = None
        self._contexts = None
        self._time_last_discovered = None

    @property
    def source_entity_id(self):
        """
        **[Required]** Gets the source_entity_id of this LogAnalyticsEntityTopologyLink.
        The log analytics entity OCID. This ID is a reference used by log analytics features and it represents
        a resource that is provisioned and managed by the customer on their premises or on the cloud.


        :return: The source_entity_id of this LogAnalyticsEntityTopologyLink.
        :rtype: str
        """
        return self._source_entity_id

    @source_entity_id.setter
    def source_entity_id(self, source_entity_id):
        """
        Sets the source_entity_id of this LogAnalyticsEntityTopologyLink.
        The log analytics entity OCID. This ID is a reference used by log analytics features and it represents
        a resource that is provisioned and managed by the customer on their premises or on the cloud.


        :param source_entity_id: The source_entity_id of this LogAnalyticsEntityTopologyLink.
        :type: str
        """
        self._source_entity_id = source_entity_id

    @property
    def destination_entity_id(self):
        """
        **[Required]** Gets the destination_entity_id of this LogAnalyticsEntityTopologyLink.
        The log analytics entity OCID. This ID is a reference used by log analytics features and it represents
        a resource that is provisioned and managed by the customer on their premises or on the cloud.


        :return: The destination_entity_id of this LogAnalyticsEntityTopologyLink.
        :rtype: str
        """
        return self._destination_entity_id

    @destination_entity_id.setter
    def destination_entity_id(self, destination_entity_id):
        """
        Sets the destination_entity_id of this LogAnalyticsEntityTopologyLink.
        The log analytics entity OCID. This ID is a reference used by log analytics features and it represents
        a resource that is provisioned and managed by the customer on their premises or on the cloud.


        :param destination_entity_id: The destination_entity_id of this LogAnalyticsEntityTopologyLink.
        :type: str
        """
        self._destination_entity_id = destination_entity_id

    @property
    def contexts(self):
        """
        Gets the contexts of this LogAnalyticsEntityTopologyLink.
        Array of log analytics entity relationship context.


        :return: The contexts of this LogAnalyticsEntityTopologyLink.
        :rtype: list[str]
        """
        return self._contexts

    @contexts.setter
    def contexts(self, contexts):
        """
        Sets the contexts of this LogAnalyticsEntityTopologyLink.
        Array of log analytics entity relationship context.


        :param contexts: The contexts of this LogAnalyticsEntityTopologyLink.
        :type: list[str]
        """
        self._contexts = contexts

    @property
    def time_last_discovered(self):
        """
        Gets the time_last_discovered of this LogAnalyticsEntityTopologyLink.
        The date and time the resource was last discovered, in the format defined by RFC3339.


        :return: The time_last_discovered of this LogAnalyticsEntityTopologyLink.
        :rtype: datetime
        """
        return self._time_last_discovered

    @time_last_discovered.setter
    def time_last_discovered(self, time_last_discovered):
        """
        Sets the time_last_discovered of this LogAnalyticsEntityTopologyLink.
        The date and time the resource was last discovered, in the format defined by RFC3339.


        :param time_last_discovered: The time_last_discovered of this LogAnalyticsEntityTopologyLink.
        :type: datetime
        """
        self._time_last_discovered = time_last_discovered

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
