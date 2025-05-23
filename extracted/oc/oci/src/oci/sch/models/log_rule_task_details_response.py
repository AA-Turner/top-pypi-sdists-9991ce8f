# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200909

from .task_details_response import TaskDetailsResponse
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LogRuleTaskDetailsResponse(TaskDetailsResponse):
    """
    The log filter task.
    For configuration instructions, see
    `Creating a Connector`__.

    __ https://docs.cloud.oracle.com/iaas/Content/connector-hub/create-service-connector.htm
    """

    def __init__(self, **kwargs):
        """
        Initializes a new LogRuleTaskDetailsResponse object with values from keyword arguments. The default value of the :py:attr:`~oci.sch.models.LogRuleTaskDetailsResponse.kind` attribute
        of this class is ``logRule`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param private_endpoint_metadata:
            The value to assign to the private_endpoint_metadata property of this LogRuleTaskDetailsResponse.
        :type private_endpoint_metadata: oci.sch.models.PrivateEndpointMetadata

        :param kind:
            The value to assign to the kind property of this LogRuleTaskDetailsResponse.
            Allowed values for this property are: "function", "logRule"
        :type kind: str

        :param condition:
            The value to assign to the condition property of this LogRuleTaskDetailsResponse.
        :type condition: str

        """
        self.swagger_types = {
            'private_endpoint_metadata': 'PrivateEndpointMetadata',
            'kind': 'str',
            'condition': 'str'
        }
        self.attribute_map = {
            'private_endpoint_metadata': 'privateEndpointMetadata',
            'kind': 'kind',
            'condition': 'condition'
        }
        self._private_endpoint_metadata = None
        self._kind = None
        self._condition = None
        self._kind = 'logRule'

    @property
    def condition(self):
        """
        **[Required]** Gets the condition of this LogRuleTaskDetailsResponse.
        A filter or mask to limit the source used in the flow defined by the connector.


        :return: The condition of this LogRuleTaskDetailsResponse.
        :rtype: str
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """
        Sets the condition of this LogRuleTaskDetailsResponse.
        A filter or mask to limit the source used in the flow defined by the connector.


        :param condition: The condition of this LogRuleTaskDetailsResponse.
        :type: str
        """
        self._condition = condition

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
