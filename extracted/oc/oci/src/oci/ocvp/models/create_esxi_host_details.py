# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20230701


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateEsxiHostDetails(object):
    """
    Details of the ESXi host to add to the Cluster.
    """

    #: A constant which can be used with the current_commitment property of a CreateEsxiHostDetails.
    #: This constant has a value of "HOUR"
    CURRENT_COMMITMENT_HOUR = "HOUR"

    #: A constant which can be used with the current_commitment property of a CreateEsxiHostDetails.
    #: This constant has a value of "MONTH"
    CURRENT_COMMITMENT_MONTH = "MONTH"

    #: A constant which can be used with the current_commitment property of a CreateEsxiHostDetails.
    #: This constant has a value of "ONE_YEAR"
    CURRENT_COMMITMENT_ONE_YEAR = "ONE_YEAR"

    #: A constant which can be used with the current_commitment property of a CreateEsxiHostDetails.
    #: This constant has a value of "THREE_YEARS"
    CURRENT_COMMITMENT_THREE_YEARS = "THREE_YEARS"

    #: A constant which can be used with the next_commitment property of a CreateEsxiHostDetails.
    #: This constant has a value of "HOUR"
    NEXT_COMMITMENT_HOUR = "HOUR"

    #: A constant which can be used with the next_commitment property of a CreateEsxiHostDetails.
    #: This constant has a value of "MONTH"
    NEXT_COMMITMENT_MONTH = "MONTH"

    #: A constant which can be used with the next_commitment property of a CreateEsxiHostDetails.
    #: This constant has a value of "ONE_YEAR"
    NEXT_COMMITMENT_ONE_YEAR = "ONE_YEAR"

    #: A constant which can be used with the next_commitment property of a CreateEsxiHostDetails.
    #: This constant has a value of "THREE_YEARS"
    NEXT_COMMITMENT_THREE_YEARS = "THREE_YEARS"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateEsxiHostDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param cluster_id:
            The value to assign to the cluster_id property of this CreateEsxiHostDetails.
        :type cluster_id: str

        :param display_name:
            The value to assign to the display_name property of this CreateEsxiHostDetails.
        :type display_name: str

        :param billing_donor_host_id:
            The value to assign to the billing_donor_host_id property of this CreateEsxiHostDetails.
        :type billing_donor_host_id: str

        :param current_commitment:
            The value to assign to the current_commitment property of this CreateEsxiHostDetails.
            Allowed values for this property are: "HOUR", "MONTH", "ONE_YEAR", "THREE_YEARS"
        :type current_commitment: str

        :param next_commitment:
            The value to assign to the next_commitment property of this CreateEsxiHostDetails.
            Allowed values for this property are: "HOUR", "MONTH", "ONE_YEAR", "THREE_YEARS"
        :type next_commitment: str

        :param compute_availability_domain:
            The value to assign to the compute_availability_domain property of this CreateEsxiHostDetails.
        :type compute_availability_domain: str

        :param host_shape_name:
            The value to assign to the host_shape_name property of this CreateEsxiHostDetails.
        :type host_shape_name: str

        :param host_ocpu_count:
            The value to assign to the host_ocpu_count property of this CreateEsxiHostDetails.
        :type host_ocpu_count: float

        :param capacity_reservation_id:
            The value to assign to the capacity_reservation_id property of this CreateEsxiHostDetails.
        :type capacity_reservation_id: str

        :param esxi_software_version:
            The value to assign to the esxi_software_version property of this CreateEsxiHostDetails.
        :type esxi_software_version: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateEsxiHostDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateEsxiHostDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'cluster_id': 'str',
            'display_name': 'str',
            'billing_donor_host_id': 'str',
            'current_commitment': 'str',
            'next_commitment': 'str',
            'compute_availability_domain': 'str',
            'host_shape_name': 'str',
            'host_ocpu_count': 'float',
            'capacity_reservation_id': 'str',
            'esxi_software_version': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }
        self.attribute_map = {
            'cluster_id': 'clusterId',
            'display_name': 'displayName',
            'billing_donor_host_id': 'billingDonorHostId',
            'current_commitment': 'currentCommitment',
            'next_commitment': 'nextCommitment',
            'compute_availability_domain': 'computeAvailabilityDomain',
            'host_shape_name': 'hostShapeName',
            'host_ocpu_count': 'hostOcpuCount',
            'capacity_reservation_id': 'capacityReservationId',
            'esxi_software_version': 'esxiSoftwareVersion',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }
        self._cluster_id = None
        self._display_name = None
        self._billing_donor_host_id = None
        self._current_commitment = None
        self._next_commitment = None
        self._compute_availability_domain = None
        self._host_shape_name = None
        self._host_ocpu_count = None
        self._capacity_reservation_id = None
        self._esxi_software_version = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def cluster_id(self):
        """
        **[Required]** Gets the cluster_id of this CreateEsxiHostDetails.
        The `OCID`__ of the Cluster to add the ESXi host to.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The cluster_id of this CreateEsxiHostDetails.
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """
        Sets the cluster_id of this CreateEsxiHostDetails.
        The `OCID`__ of the Cluster to add the ESXi host to.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param cluster_id: The cluster_id of this CreateEsxiHostDetails.
        :type: str
        """
        self._cluster_id = cluster_id

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateEsxiHostDetails.
        A descriptive name for the ESXi host. It's changeable.
        Esxi Host name requirements are 1-16 character length limit, Must start with a letter,
        Must be English letters, numbers, - only, No repeating hyphens, Must be unique within the Cluster.

        If this attribute is not specified, the Cluster's `instanceDisplayNamePrefix` attribute is used
        to name and incrementally number the ESXi host. For example, if you're creating the fourth
        ESXi host in the Cluster, and `instanceDisplayNamePrefix` is `MyCluster`, the host's display
        name is `MyCluster-4`.

        Avoid entering confidential information.


        :return: The display_name of this CreateEsxiHostDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateEsxiHostDetails.
        A descriptive name for the ESXi host. It's changeable.
        Esxi Host name requirements are 1-16 character length limit, Must start with a letter,
        Must be English letters, numbers, - only, No repeating hyphens, Must be unique within the Cluster.

        If this attribute is not specified, the Cluster's `instanceDisplayNamePrefix` attribute is used
        to name and incrementally number the ESXi host. For example, if you're creating the fourth
        ESXi host in the Cluster, and `instanceDisplayNamePrefix` is `MyCluster`, the host's display
        name is `MyCluster-4`.

        Avoid entering confidential information.


        :param display_name: The display_name of this CreateEsxiHostDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def billing_donor_host_id(self):
        """
        Gets the billing_donor_host_id of this CreateEsxiHostDetails.
        The `OCID`__ of the deleted ESXi Host with LeftOver billing cycle.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The billing_donor_host_id of this CreateEsxiHostDetails.
        :rtype: str
        """
        return self._billing_donor_host_id

    @billing_donor_host_id.setter
    def billing_donor_host_id(self, billing_donor_host_id):
        """
        Sets the billing_donor_host_id of this CreateEsxiHostDetails.
        The `OCID`__ of the deleted ESXi Host with LeftOver billing cycle.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param billing_donor_host_id: The billing_donor_host_id of this CreateEsxiHostDetails.
        :type: str
        """
        self._billing_donor_host_id = billing_donor_host_id

    @property
    def current_commitment(self):
        """
        Gets the current_commitment of this CreateEsxiHostDetails.
        The billing option currently used by the ESXi host.
        :func:`list_supported_commitments`.

        Allowed values for this property are: "HOUR", "MONTH", "ONE_YEAR", "THREE_YEARS"


        :return: The current_commitment of this CreateEsxiHostDetails.
        :rtype: str
        """
        return self._current_commitment

    @current_commitment.setter
    def current_commitment(self, current_commitment):
        """
        Sets the current_commitment of this CreateEsxiHostDetails.
        The billing option currently used by the ESXi host.
        :func:`list_supported_commitments`.


        :param current_commitment: The current_commitment of this CreateEsxiHostDetails.
        :type: str
        """
        allowed_values = ["HOUR", "MONTH", "ONE_YEAR", "THREE_YEARS"]
        if not value_allowed_none_or_none_sentinel(current_commitment, allowed_values):
            raise ValueError(
                f"Invalid value for `current_commitment`, must be None or one of {allowed_values}"
            )
        self._current_commitment = current_commitment

    @property
    def next_commitment(self):
        """
        Gets the next_commitment of this CreateEsxiHostDetails.
        The billing option to switch to after the existing billing cycle ends.
        If `nextCommitment` is null or empty, `currentCommitment` continues to the next billing cycle.
        :func:`list_supported_commitments`.

        Allowed values for this property are: "HOUR", "MONTH", "ONE_YEAR", "THREE_YEARS"


        :return: The next_commitment of this CreateEsxiHostDetails.
        :rtype: str
        """
        return self._next_commitment

    @next_commitment.setter
    def next_commitment(self, next_commitment):
        """
        Sets the next_commitment of this CreateEsxiHostDetails.
        The billing option to switch to after the existing billing cycle ends.
        If `nextCommitment` is null or empty, `currentCommitment` continues to the next billing cycle.
        :func:`list_supported_commitments`.


        :param next_commitment: The next_commitment of this CreateEsxiHostDetails.
        :type: str
        """
        allowed_values = ["HOUR", "MONTH", "ONE_YEAR", "THREE_YEARS"]
        if not value_allowed_none_or_none_sentinel(next_commitment, allowed_values):
            raise ValueError(
                f"Invalid value for `next_commitment`, must be None or one of {allowed_values}"
            )
        self._next_commitment = next_commitment

    @property
    def compute_availability_domain(self):
        """
        Gets the compute_availability_domain of this CreateEsxiHostDetails.
        The availability domain to create the ESXi host in.
        If keep empty, for AD-specific Cluster, new ESXi host will be created in the same availability domain;
        for multi-AD Cluster, new ESXi host will be auto assigned to the next availability domain following evenly distribution strategy.


        :return: The compute_availability_domain of this CreateEsxiHostDetails.
        :rtype: str
        """
        return self._compute_availability_domain

    @compute_availability_domain.setter
    def compute_availability_domain(self, compute_availability_domain):
        """
        Sets the compute_availability_domain of this CreateEsxiHostDetails.
        The availability domain to create the ESXi host in.
        If keep empty, for AD-specific Cluster, new ESXi host will be created in the same availability domain;
        for multi-AD Cluster, new ESXi host will be auto assigned to the next availability domain following evenly distribution strategy.


        :param compute_availability_domain: The compute_availability_domain of this CreateEsxiHostDetails.
        :type: str
        """
        self._compute_availability_domain = compute_availability_domain

    @property
    def host_shape_name(self):
        """
        Gets the host_shape_name of this CreateEsxiHostDetails.
        The compute shape name of the ESXi host.
        :func:`list_supported_host_shapes`.


        :return: The host_shape_name of this CreateEsxiHostDetails.
        :rtype: str
        """
        return self._host_shape_name

    @host_shape_name.setter
    def host_shape_name(self, host_shape_name):
        """
        Sets the host_shape_name of this CreateEsxiHostDetails.
        The compute shape name of the ESXi host.
        :func:`list_supported_host_shapes`.


        :param host_shape_name: The host_shape_name of this CreateEsxiHostDetails.
        :type: str
        """
        self._host_shape_name = host_shape_name

    @property
    def host_ocpu_count(self):
        """
        Gets the host_ocpu_count of this CreateEsxiHostDetails.
        The OCPU count of the ESXi host.


        :return: The host_ocpu_count of this CreateEsxiHostDetails.
        :rtype: float
        """
        return self._host_ocpu_count

    @host_ocpu_count.setter
    def host_ocpu_count(self, host_ocpu_count):
        """
        Sets the host_ocpu_count of this CreateEsxiHostDetails.
        The OCPU count of the ESXi host.


        :param host_ocpu_count: The host_ocpu_count of this CreateEsxiHostDetails.
        :type: float
        """
        self._host_ocpu_count = host_ocpu_count

    @property
    def capacity_reservation_id(self):
        """
        Gets the capacity_reservation_id of this CreateEsxiHostDetails.
        The `OCID`__ of the Capacity Reservation.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The capacity_reservation_id of this CreateEsxiHostDetails.
        :rtype: str
        """
        return self._capacity_reservation_id

    @capacity_reservation_id.setter
    def capacity_reservation_id(self, capacity_reservation_id):
        """
        Sets the capacity_reservation_id of this CreateEsxiHostDetails.
        The `OCID`__ of the Capacity Reservation.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param capacity_reservation_id: The capacity_reservation_id of this CreateEsxiHostDetails.
        :type: str
        """
        self._capacity_reservation_id = capacity_reservation_id

    @property
    def esxi_software_version(self):
        """
        Gets the esxi_software_version of this CreateEsxiHostDetails.
        The ESXi software bundle to install on the ESXi host.
        Only versions under the same vmwareSoftwareVersion and have been validate by Oracle Cloud VMware Solution will be accepted.
        To get a list of the available versions, use
        :func:`list_supported_vmware_software_versions`.


        :return: The esxi_software_version of this CreateEsxiHostDetails.
        :rtype: str
        """
        return self._esxi_software_version

    @esxi_software_version.setter
    def esxi_software_version(self, esxi_software_version):
        """
        Sets the esxi_software_version of this CreateEsxiHostDetails.
        The ESXi software bundle to install on the ESXi host.
        Only versions under the same vmwareSoftwareVersion and have been validate by Oracle Cloud VMware Solution will be accepted.
        To get a list of the available versions, use
        :func:`list_supported_vmware_software_versions`.


        :param esxi_software_version: The esxi_software_version of this CreateEsxiHostDetails.
        :type: str
        """
        self._esxi_software_version = esxi_software_version

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateEsxiHostDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateEsxiHostDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateEsxiHostDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateEsxiHostDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateEsxiHostDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateEsxiHostDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateEsxiHostDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateEsxiHostDetails.
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
