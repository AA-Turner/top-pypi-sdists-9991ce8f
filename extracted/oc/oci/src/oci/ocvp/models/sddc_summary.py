# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20230701


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SddcSummary(object):
    """
    A summary of the SDDC.
    """

    #: A constant which can be used with the hcx_mode property of a SddcSummary.
    #: This constant has a value of "DISABLED"
    HCX_MODE_DISABLED = "DISABLED"

    #: A constant which can be used with the hcx_mode property of a SddcSummary.
    #: This constant has a value of "ADVANCED"
    HCX_MODE_ADVANCED = "ADVANCED"

    #: A constant which can be used with the hcx_mode property of a SddcSummary.
    #: This constant has a value of "ENTERPRISE"
    HCX_MODE_ENTERPRISE = "ENTERPRISE"

    #: A constant which can be used with the lifecycle_state property of a SddcSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a SddcSummary.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a SddcSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a SddcSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a SddcSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a SddcSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new SddcSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this SddcSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this SddcSummary.
        :type display_name: str

        :param vmware_software_version:
            The value to assign to the vmware_software_version property of this SddcSummary.
        :type vmware_software_version: str

        :param compartment_id:
            The value to assign to the compartment_id property of this SddcSummary.
        :type compartment_id: str

        :param clusters_count:
            The value to assign to the clusters_count property of this SddcSummary.
        :type clusters_count: int

        :param hcx_fqdn:
            The value to assign to the hcx_fqdn property of this SddcSummary.
        :type hcx_fqdn: str

        :param hcx_mode:
            The value to assign to the hcx_mode property of this SddcSummary.
            Allowed values for this property are: "DISABLED", "ADVANCED", "ENTERPRISE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type hcx_mode: str

        :param vcenter_fqdn:
            The value to assign to the vcenter_fqdn property of this SddcSummary.
        :type vcenter_fqdn: str

        :param nsx_manager_fqdn:
            The value to assign to the nsx_manager_fqdn property of this SddcSummary.
        :type nsx_manager_fqdn: str

        :param time_created:
            The value to assign to the time_created property of this SddcSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this SddcSummary.
        :type time_updated: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this SddcSummary.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param is_single_host_sddc:
            The value to assign to the is_single_host_sddc property of this SddcSummary.
        :type is_single_host_sddc: bool

        :param freeform_tags:
            The value to assign to the freeform_tags property of this SddcSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this SddcSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this SddcSummary.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'vmware_software_version': 'str',
            'compartment_id': 'str',
            'clusters_count': 'int',
            'hcx_fqdn': 'str',
            'hcx_mode': 'str',
            'vcenter_fqdn': 'str',
            'nsx_manager_fqdn': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_state': 'str',
            'is_single_host_sddc': 'bool',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }
        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'vmware_software_version': 'vmwareSoftwareVersion',
            'compartment_id': 'compartmentId',
            'clusters_count': 'clustersCount',
            'hcx_fqdn': 'hcxFqdn',
            'hcx_mode': 'hcxMode',
            'vcenter_fqdn': 'vcenterFqdn',
            'nsx_manager_fqdn': 'nsxManagerFqdn',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_state': 'lifecycleState',
            'is_single_host_sddc': 'isSingleHostSddc',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }
        self._id = None
        self._display_name = None
        self._vmware_software_version = None
        self._compartment_id = None
        self._clusters_count = None
        self._hcx_fqdn = None
        self._hcx_mode = None
        self._vcenter_fqdn = None
        self._nsx_manager_fqdn = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_state = None
        self._is_single_host_sddc = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this SddcSummary.
        The `OCID`__ of the compartment that
        contains the SDDC.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this SddcSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SddcSummary.
        The `OCID`__ of the compartment that
        contains the SDDC.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this SddcSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this SddcSummary.
        A descriptive name for the SDDC. It must be unique, start with a letter, and contain only letters, digits,
        whitespaces, dashes and underscores.
        Avoid entering confidential information.


        :return: The display_name of this SddcSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this SddcSummary.
        A descriptive name for the SDDC. It must be unique, start with a letter, and contain only letters, digits,
        whitespaces, dashes and underscores.
        Avoid entering confidential information.


        :param display_name: The display_name of this SddcSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def vmware_software_version(self):
        """
        **[Required]** Gets the vmware_software_version of this SddcSummary.
        In general, this is a specific version of bundled VMware software supported by
        Oracle Cloud VMware Solution (see
        :func:`list_supported_vmware_software_versions`).

        This attribute is not guaranteed to reflect the version of
        software currently installed on the ESXi hosts in the SDDC. The purpose
        of this attribute is to show the version of software that the Oracle
        Cloud VMware Solution will install on any new ESXi hosts that you *add to this
        SDDC in the future* with :func:`create_esxi_host`.

        Therefore, if you upgrade the existing ESXi hosts in the SDDC to use a newer
        version of bundled VMware software supported by the Oracle Cloud VMware Solution, you
        should use :func:`update_sddc` to update the SDDC's
        `vmwareSoftwareVersion` with that new version.


        :return: The vmware_software_version of this SddcSummary.
        :rtype: str
        """
        return self._vmware_software_version

    @vmware_software_version.setter
    def vmware_software_version(self, vmware_software_version):
        """
        Sets the vmware_software_version of this SddcSummary.
        In general, this is a specific version of bundled VMware software supported by
        Oracle Cloud VMware Solution (see
        :func:`list_supported_vmware_software_versions`).

        This attribute is not guaranteed to reflect the version of
        software currently installed on the ESXi hosts in the SDDC. The purpose
        of this attribute is to show the version of software that the Oracle
        Cloud VMware Solution will install on any new ESXi hosts that you *add to this
        SDDC in the future* with :func:`create_esxi_host`.

        Therefore, if you upgrade the existing ESXi hosts in the SDDC to use a newer
        version of bundled VMware software supported by the Oracle Cloud VMware Solution, you
        should use :func:`update_sddc` to update the SDDC's
        `vmwareSoftwareVersion` with that new version.


        :param vmware_software_version: The vmware_software_version of this SddcSummary.
        :type: str
        """
        self._vmware_software_version = vmware_software_version

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this SddcSummary.
        The `OCID`__ of the compartment that
        contains the SDDC.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this SddcSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this SddcSummary.
        The `OCID`__ of the compartment that
        contains the SDDC.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this SddcSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def clusters_count(self):
        """
        **[Required]** Gets the clusters_count of this SddcSummary.
        The number of ESXi hosts in the SDDC.


        :return: The clusters_count of this SddcSummary.
        :rtype: int
        """
        return self._clusters_count

    @clusters_count.setter
    def clusters_count(self, clusters_count):
        """
        Sets the clusters_count of this SddcSummary.
        The number of ESXi hosts in the SDDC.


        :param clusters_count: The clusters_count of this SddcSummary.
        :type: int
        """
        self._clusters_count = clusters_count

    @property
    def hcx_fqdn(self):
        """
        Gets the hcx_fqdn of this SddcSummary.
        HCX Fully Qualified Domain Name


        :return: The hcx_fqdn of this SddcSummary.
        :rtype: str
        """
        return self._hcx_fqdn

    @hcx_fqdn.setter
    def hcx_fqdn(self, hcx_fqdn):
        """
        Sets the hcx_fqdn of this SddcSummary.
        HCX Fully Qualified Domain Name


        :param hcx_fqdn: The hcx_fqdn of this SddcSummary.
        :type: str
        """
        self._hcx_fqdn = hcx_fqdn

    @property
    def hcx_mode(self):
        """
        Gets the hcx_mode of this SddcSummary.
        HCX configuration of the SDDC.

        Allowed values for this property are: "DISABLED", "ADVANCED", "ENTERPRISE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The hcx_mode of this SddcSummary.
        :rtype: str
        """
        return self._hcx_mode

    @hcx_mode.setter
    def hcx_mode(self, hcx_mode):
        """
        Sets the hcx_mode of this SddcSummary.
        HCX configuration of the SDDC.


        :param hcx_mode: The hcx_mode of this SddcSummary.
        :type: str
        """
        allowed_values = ["DISABLED", "ADVANCED", "ENTERPRISE"]
        if not value_allowed_none_or_none_sentinel(hcx_mode, allowed_values):
            hcx_mode = 'UNKNOWN_ENUM_VALUE'
        self._hcx_mode = hcx_mode

    @property
    def vcenter_fqdn(self):
        """
        Gets the vcenter_fqdn of this SddcSummary.
        FQDN for vCenter

        Example: `vcenter-my-sddc.sddc.us-phoenix-1.oraclecloud.com`


        :return: The vcenter_fqdn of this SddcSummary.
        :rtype: str
        """
        return self._vcenter_fqdn

    @vcenter_fqdn.setter
    def vcenter_fqdn(self, vcenter_fqdn):
        """
        Sets the vcenter_fqdn of this SddcSummary.
        FQDN for vCenter

        Example: `vcenter-my-sddc.sddc.us-phoenix-1.oraclecloud.com`


        :param vcenter_fqdn: The vcenter_fqdn of this SddcSummary.
        :type: str
        """
        self._vcenter_fqdn = vcenter_fqdn

    @property
    def nsx_manager_fqdn(self):
        """
        Gets the nsx_manager_fqdn of this SddcSummary.
        FQDN for NSX Manager

        Example: `nsx-my-sddc.sddc.us-phoenix-1.oraclecloud.com`


        :return: The nsx_manager_fqdn of this SddcSummary.
        :rtype: str
        """
        return self._nsx_manager_fqdn

    @nsx_manager_fqdn.setter
    def nsx_manager_fqdn(self, nsx_manager_fqdn):
        """
        Sets the nsx_manager_fqdn of this SddcSummary.
        FQDN for NSX Manager

        Example: `nsx-my-sddc.sddc.us-phoenix-1.oraclecloud.com`


        :param nsx_manager_fqdn: The nsx_manager_fqdn of this SddcSummary.
        :type: str
        """
        self._nsx_manager_fqdn = nsx_manager_fqdn

    @property
    def time_created(self):
        """
        Gets the time_created of this SddcSummary.
        The date and time the SDDC was created, in the format defined by
        `RFC3339`__.

        Example: `2016-08-25T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this SddcSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this SddcSummary.
        The date and time the SDDC was created, in the format defined by
        `RFC3339`__.

        Example: `2016-08-25T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this SddcSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this SddcSummary.
        The date and time the SDDC was updated, in the format defined by
        `RFC3339`__.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_updated of this SddcSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this SddcSummary.
        The date and time the SDDC was updated, in the format defined by
        `RFC3339`__.

        __ https://tools.ietf.org/html/rfc3339


        :param time_updated: The time_updated of this SddcSummary.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this SddcSummary.
        The current state of the SDDC.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this SddcSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this SddcSummary.
        The current state of the SDDC.


        :param lifecycle_state: The lifecycle_state of this SddcSummary.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def is_single_host_sddc(self):
        """
        Gets the is_single_host_sddc of this SddcSummary.
        Indicates whether this SDDC is designated for only single ESXi host.


        :return: The is_single_host_sddc of this SddcSummary.
        :rtype: bool
        """
        return self._is_single_host_sddc

    @is_single_host_sddc.setter
    def is_single_host_sddc(self, is_single_host_sddc):
        """
        Sets the is_single_host_sddc of this SddcSummary.
        Indicates whether this SDDC is designated for only single ESXi host.


        :param is_single_host_sddc: The is_single_host_sddc of this SddcSummary.
        :type: bool
        """
        self._is_single_host_sddc = is_single_host_sddc

    @property
    def freeform_tags(self):
        """
        **[Required]** Gets the freeform_tags of this SddcSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this SddcSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this SddcSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this SddcSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        **[Required]** Gets the defined_tags of this SddcSummary.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this SddcSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this SddcSummary.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this SddcSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this SddcSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{orcl-cloud: {free-tier-retain: true}}`


        :return: The system_tags of this SddcSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this SddcSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{orcl-cloud: {free-tier-retain: true}}`


        :param system_tags: The system_tags of this SddcSummary.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
