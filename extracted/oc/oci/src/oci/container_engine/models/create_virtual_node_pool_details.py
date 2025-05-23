# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20180222


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateVirtualNodePoolDetails(object):
    """
    The properties that define a request to create a virtual node pool.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateVirtualNodePoolDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateVirtualNodePoolDetails.
        :type compartment_id: str

        :param cluster_id:
            The value to assign to the cluster_id property of this CreateVirtualNodePoolDetails.
        :type cluster_id: str

        :param display_name:
            The value to assign to the display_name property of this CreateVirtualNodePoolDetails.
        :type display_name: str

        :param initial_virtual_node_labels:
            The value to assign to the initial_virtual_node_labels property of this CreateVirtualNodePoolDetails.
        :type initial_virtual_node_labels: list[oci.container_engine.models.InitialVirtualNodeLabel]

        :param taints:
            The value to assign to the taints property of this CreateVirtualNodePoolDetails.
        :type taints: list[oci.container_engine.models.Taint]

        :param size:
            The value to assign to the size property of this CreateVirtualNodePoolDetails.
        :type size: int

        :param placement_configurations:
            The value to assign to the placement_configurations property of this CreateVirtualNodePoolDetails.
        :type placement_configurations: list[oci.container_engine.models.PlacementConfiguration]

        :param nsg_ids:
            The value to assign to the nsg_ids property of this CreateVirtualNodePoolDetails.
        :type nsg_ids: list[str]

        :param pod_configuration:
            The value to assign to the pod_configuration property of this CreateVirtualNodePoolDetails.
        :type pod_configuration: oci.container_engine.models.PodConfiguration

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateVirtualNodePoolDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateVirtualNodePoolDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param virtual_node_tags:
            The value to assign to the virtual_node_tags property of this CreateVirtualNodePoolDetails.
        :type virtual_node_tags: oci.container_engine.models.VirtualNodeTags

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'cluster_id': 'str',
            'display_name': 'str',
            'initial_virtual_node_labels': 'list[InitialVirtualNodeLabel]',
            'taints': 'list[Taint]',
            'size': 'int',
            'placement_configurations': 'list[PlacementConfiguration]',
            'nsg_ids': 'list[str]',
            'pod_configuration': 'PodConfiguration',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'virtual_node_tags': 'VirtualNodeTags'
        }
        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'cluster_id': 'clusterId',
            'display_name': 'displayName',
            'initial_virtual_node_labels': 'initialVirtualNodeLabels',
            'taints': 'taints',
            'size': 'size',
            'placement_configurations': 'placementConfigurations',
            'nsg_ids': 'nsgIds',
            'pod_configuration': 'podConfiguration',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'virtual_node_tags': 'virtualNodeTags'
        }
        self._compartment_id = None
        self._cluster_id = None
        self._display_name = None
        self._initial_virtual_node_labels = None
        self._taints = None
        self._size = None
        self._placement_configurations = None
        self._nsg_ids = None
        self._pod_configuration = None
        self._freeform_tags = None
        self._defined_tags = None
        self._virtual_node_tags = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateVirtualNodePoolDetails.
        Compartment of the virtual node pool.


        :return: The compartment_id of this CreateVirtualNodePoolDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateVirtualNodePoolDetails.
        Compartment of the virtual node pool.


        :param compartment_id: The compartment_id of this CreateVirtualNodePoolDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def cluster_id(self):
        """
        **[Required]** Gets the cluster_id of this CreateVirtualNodePoolDetails.
        The cluster the virtual node pool is associated with. A virtual node pool can only be associated with one cluster.


        :return: The cluster_id of this CreateVirtualNodePoolDetails.
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """
        Sets the cluster_id of this CreateVirtualNodePoolDetails.
        The cluster the virtual node pool is associated with. A virtual node pool can only be associated with one cluster.


        :param cluster_id: The cluster_id of this CreateVirtualNodePoolDetails.
        :type: str
        """
        self._cluster_id = cluster_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this CreateVirtualNodePoolDetails.
        Display name of the virtual node pool. This is a non-unique value.


        :return: The display_name of this CreateVirtualNodePoolDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateVirtualNodePoolDetails.
        Display name of the virtual node pool. This is a non-unique value.


        :param display_name: The display_name of this CreateVirtualNodePoolDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def initial_virtual_node_labels(self):
        """
        Gets the initial_virtual_node_labels of this CreateVirtualNodePoolDetails.
        Initial labels that will be added to the Kubernetes Virtual Node object when it registers.


        :return: The initial_virtual_node_labels of this CreateVirtualNodePoolDetails.
        :rtype: list[oci.container_engine.models.InitialVirtualNodeLabel]
        """
        return self._initial_virtual_node_labels

    @initial_virtual_node_labels.setter
    def initial_virtual_node_labels(self, initial_virtual_node_labels):
        """
        Sets the initial_virtual_node_labels of this CreateVirtualNodePoolDetails.
        Initial labels that will be added to the Kubernetes Virtual Node object when it registers.


        :param initial_virtual_node_labels: The initial_virtual_node_labels of this CreateVirtualNodePoolDetails.
        :type: list[oci.container_engine.models.InitialVirtualNodeLabel]
        """
        self._initial_virtual_node_labels = initial_virtual_node_labels

    @property
    def taints(self):
        """
        Gets the taints of this CreateVirtualNodePoolDetails.
        A taint is a collection of <key, value, effect>. These taints will be applied to the Virtual Nodes of this Virtual Node Pool for Kubernetes scheduling.


        :return: The taints of this CreateVirtualNodePoolDetails.
        :rtype: list[oci.container_engine.models.Taint]
        """
        return self._taints

    @taints.setter
    def taints(self, taints):
        """
        Sets the taints of this CreateVirtualNodePoolDetails.
        A taint is a collection of <key, value, effect>. These taints will be applied to the Virtual Nodes of this Virtual Node Pool for Kubernetes scheduling.


        :param taints: The taints of this CreateVirtualNodePoolDetails.
        :type: list[oci.container_engine.models.Taint]
        """
        self._taints = taints

    @property
    def size(self):
        """
        Gets the size of this CreateVirtualNodePoolDetails.
        The number of Virtual Nodes that should be in the Virtual Node Pool. The placement configurations determine where these virtual nodes are placed.


        :return: The size of this CreateVirtualNodePoolDetails.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size of this CreateVirtualNodePoolDetails.
        The number of Virtual Nodes that should be in the Virtual Node Pool. The placement configurations determine where these virtual nodes are placed.


        :param size: The size of this CreateVirtualNodePoolDetails.
        :type: int
        """
        self._size = size

    @property
    def placement_configurations(self):
        """
        **[Required]** Gets the placement_configurations of this CreateVirtualNodePoolDetails.
        The list of placement configurations which determines where Virtual Nodes will be provisioned across as it relates to the subnet and availability domains. The size attribute determines how many we evenly spread across these placement configurations


        :return: The placement_configurations of this CreateVirtualNodePoolDetails.
        :rtype: list[oci.container_engine.models.PlacementConfiguration]
        """
        return self._placement_configurations

    @placement_configurations.setter
    def placement_configurations(self, placement_configurations):
        """
        Sets the placement_configurations of this CreateVirtualNodePoolDetails.
        The list of placement configurations which determines where Virtual Nodes will be provisioned across as it relates to the subnet and availability domains. The size attribute determines how many we evenly spread across these placement configurations


        :param placement_configurations: The placement_configurations of this CreateVirtualNodePoolDetails.
        :type: list[oci.container_engine.models.PlacementConfiguration]
        """
        self._placement_configurations = placement_configurations

    @property
    def nsg_ids(self):
        """
        Gets the nsg_ids of this CreateVirtualNodePoolDetails.
        List of network security group id's applied to the Virtual Node VNIC.


        :return: The nsg_ids of this CreateVirtualNodePoolDetails.
        :rtype: list[str]
        """
        return self._nsg_ids

    @nsg_ids.setter
    def nsg_ids(self, nsg_ids):
        """
        Sets the nsg_ids of this CreateVirtualNodePoolDetails.
        List of network security group id's applied to the Virtual Node VNIC.


        :param nsg_ids: The nsg_ids of this CreateVirtualNodePoolDetails.
        :type: list[str]
        """
        self._nsg_ids = nsg_ids

    @property
    def pod_configuration(self):
        """
        Gets the pod_configuration of this CreateVirtualNodePoolDetails.
        The pod configuration for pods run on virtual nodes of this virtual node pool.


        :return: The pod_configuration of this CreateVirtualNodePoolDetails.
        :rtype: oci.container_engine.models.PodConfiguration
        """
        return self._pod_configuration

    @pod_configuration.setter
    def pod_configuration(self, pod_configuration):
        """
        Sets the pod_configuration of this CreateVirtualNodePoolDetails.
        The pod configuration for pods run on virtual nodes of this virtual node pool.


        :param pod_configuration: The pod_configuration of this CreateVirtualNodePoolDetails.
        :type: oci.container_engine.models.PodConfiguration
        """
        self._pod_configuration = pod_configuration

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateVirtualNodePoolDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateVirtualNodePoolDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateVirtualNodePoolDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateVirtualNodePoolDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateVirtualNodePoolDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateVirtualNodePoolDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateVirtualNodePoolDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateVirtualNodePoolDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def virtual_node_tags(self):
        """
        Gets the virtual_node_tags of this CreateVirtualNodePoolDetails.

        :return: The virtual_node_tags of this CreateVirtualNodePoolDetails.
        :rtype: oci.container_engine.models.VirtualNodeTags
        """
        return self._virtual_node_tags

    @virtual_node_tags.setter
    def virtual_node_tags(self, virtual_node_tags):
        """
        Sets the virtual_node_tags of this CreateVirtualNodePoolDetails.

        :param virtual_node_tags: The virtual_node_tags of this CreateVirtualNodePoolDetails.
        :type: oci.container_engine.models.VirtualNodeTags
        """
        self._virtual_node_tags = virtual_node_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
