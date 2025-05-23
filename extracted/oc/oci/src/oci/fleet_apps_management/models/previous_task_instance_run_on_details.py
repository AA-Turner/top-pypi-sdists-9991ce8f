# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20250228

from .run_on_details import RunOnDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PreviousTaskInstanceRunOnDetails(RunOnDetails):
    """
    Time-based pause details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PreviousTaskInstanceRunOnDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.fleet_apps_management.models.PreviousTaskInstanceRunOnDetails.kind` attribute
        of this class is ``PREVIOUS_TASK_INSTANCES`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param kind:
            The value to assign to the kind property of this PreviousTaskInstanceRunOnDetails.
            Allowed values for this property are: "SCHEDULED_INSTANCES", "SELF_HOSTED_INSTANCES", "PREVIOUS_TASK_INSTANCES"
        :type kind: str

        :param previous_task_instance_details:
            The value to assign to the previous_task_instance_details property of this PreviousTaskInstanceRunOnDetails.
        :type previous_task_instance_details: list[oci.fleet_apps_management.models.PreviousTaskInstanceDetails]

        """
        self.swagger_types = {
            'kind': 'str',
            'previous_task_instance_details': 'list[PreviousTaskInstanceDetails]'
        }
        self.attribute_map = {
            'kind': 'kind',
            'previous_task_instance_details': 'previousTaskInstanceDetails'
        }
        self._kind = None
        self._previous_task_instance_details = None
        self._kind = 'PREVIOUS_TASK_INSTANCES'

    @property
    def previous_task_instance_details(self):
        """
        **[Required]** Gets the previous_task_instance_details of this PreviousTaskInstanceRunOnDetails.
        Previous Task Instance Details


        :return: The previous_task_instance_details of this PreviousTaskInstanceRunOnDetails.
        :rtype: list[oci.fleet_apps_management.models.PreviousTaskInstanceDetails]
        """
        return self._previous_task_instance_details

    @previous_task_instance_details.setter
    def previous_task_instance_details(self, previous_task_instance_details):
        """
        Sets the previous_task_instance_details of this PreviousTaskInstanceRunOnDetails.
        Previous Task Instance Details


        :param previous_task_instance_details: The previous_task_instance_details of this PreviousTaskInstanceRunOnDetails.
        :type: list[oci.fleet_apps_management.models.PreviousTaskInstanceDetails]
        """
        self._previous_task_instance_details = previous_task_instance_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
