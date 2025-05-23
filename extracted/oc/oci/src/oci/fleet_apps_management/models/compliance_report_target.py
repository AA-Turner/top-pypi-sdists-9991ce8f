# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20250228


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ComplianceReportTarget(object):
    """
    Details of the target and patches.
    """

    #: A constant which can be used with the compliance_state property of a ComplianceReportTarget.
    #: This constant has a value of "UNKNOWN"
    COMPLIANCE_STATE_UNKNOWN = "UNKNOWN"

    #: A constant which can be used with the compliance_state property of a ComplianceReportTarget.
    #: This constant has a value of "COMPLIANT"
    COMPLIANCE_STATE_COMPLIANT = "COMPLIANT"

    #: A constant which can be used with the compliance_state property of a ComplianceReportTarget.
    #: This constant has a value of "NON_COMPLIANT"
    COMPLIANCE_STATE_NON_COMPLIANT = "NON_COMPLIANT"

    #: A constant which can be used with the compliance_state property of a ComplianceReportTarget.
    #: This constant has a value of "WARNING"
    COMPLIANCE_STATE_WARNING = "WARNING"

    def __init__(self, **kwargs):
        """
        Initializes a new ComplianceReportTarget object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param target_id:
            The value to assign to the target_id property of this ComplianceReportTarget.
        :type target_id: str

        :param target_name:
            The value to assign to the target_name property of this ComplianceReportTarget.
        :type target_name: str

        :param version:
            The value to assign to the version property of this ComplianceReportTarget.
        :type version: str

        :param compliance_state:
            The value to assign to the compliance_state property of this ComplianceReportTarget.
            Allowed values for this property are: "UNKNOWN", "COMPLIANT", "NON_COMPLIANT", "WARNING", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type compliance_state: str

        :param installed_patches:
            The value to assign to the installed_patches property of this ComplianceReportTarget.
        :type installed_patches: list[oci.fleet_apps_management.models.ComplianceReportPatchDetail]

        :param recommended_patches:
            The value to assign to the recommended_patches property of this ComplianceReportTarget.
        :type recommended_patches: list[oci.fleet_apps_management.models.ComplianceReportPatchDetail]

        """
        self.swagger_types = {
            'target_id': 'str',
            'target_name': 'str',
            'version': 'str',
            'compliance_state': 'str',
            'installed_patches': 'list[ComplianceReportPatchDetail]',
            'recommended_patches': 'list[ComplianceReportPatchDetail]'
        }
        self.attribute_map = {
            'target_id': 'targetId',
            'target_name': 'targetName',
            'version': 'version',
            'compliance_state': 'complianceState',
            'installed_patches': 'installedPatches',
            'recommended_patches': 'recommendedPatches'
        }
        self._target_id = None
        self._target_name = None
        self._version = None
        self._compliance_state = None
        self._installed_patches = None
        self._recommended_patches = None

    @property
    def target_id(self):
        """
        **[Required]** Gets the target_id of this ComplianceReportTarget.
        Target Identifier.Can be the target name if a separate ID is not available.


        :return: The target_id of this ComplianceReportTarget.
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """
        Sets the target_id of this ComplianceReportTarget.
        Target Identifier.Can be the target name if a separate ID is not available.


        :param target_id: The target_id of this ComplianceReportTarget.
        :type: str
        """
        self._target_id = target_id

    @property
    def target_name(self):
        """
        **[Required]** Gets the target_name of this ComplianceReportTarget.
        Target Name.


        :return: The target_name of this ComplianceReportTarget.
        :rtype: str
        """
        return self._target_name

    @target_name.setter
    def target_name(self, target_name):
        """
        Sets the target_name of this ComplianceReportTarget.
        Target Name.


        :param target_name: The target_name of this ComplianceReportTarget.
        :type: str
        """
        self._target_name = target_name

    @property
    def version(self):
        """
        Gets the version of this ComplianceReportTarget.
        Current version of the target.


        :return: The version of this ComplianceReportTarget.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this ComplianceReportTarget.
        Current version of the target.


        :param version: The version of this ComplianceReportTarget.
        :type: str
        """
        self._version = version

    @property
    def compliance_state(self):
        """
        **[Required]** Gets the compliance_state of this ComplianceReportTarget.
        The last known compliance state of the target.

        Allowed values for this property are: "UNKNOWN", "COMPLIANT", "NON_COMPLIANT", "WARNING", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The compliance_state of this ComplianceReportTarget.
        :rtype: str
        """
        return self._compliance_state

    @compliance_state.setter
    def compliance_state(self, compliance_state):
        """
        Sets the compliance_state of this ComplianceReportTarget.
        The last known compliance state of the target.


        :param compliance_state: The compliance_state of this ComplianceReportTarget.
        :type: str
        """
        allowed_values = ["UNKNOWN", "COMPLIANT", "NON_COMPLIANT", "WARNING"]
        if not value_allowed_none_or_none_sentinel(compliance_state, allowed_values):
            compliance_state = 'UNKNOWN_ENUM_VALUE'
        self._compliance_state = compliance_state

    @property
    def installed_patches(self):
        """
        Gets the installed_patches of this ComplianceReportTarget.
        Installed Patches for the Target.


        :return: The installed_patches of this ComplianceReportTarget.
        :rtype: list[oci.fleet_apps_management.models.ComplianceReportPatchDetail]
        """
        return self._installed_patches

    @installed_patches.setter
    def installed_patches(self, installed_patches):
        """
        Sets the installed_patches of this ComplianceReportTarget.
        Installed Patches for the Target.


        :param installed_patches: The installed_patches of this ComplianceReportTarget.
        :type: list[oci.fleet_apps_management.models.ComplianceReportPatchDetail]
        """
        self._installed_patches = installed_patches

    @property
    def recommended_patches(self):
        """
        Gets the recommended_patches of this ComplianceReportTarget.
        Recommended Patches for the Target.


        :return: The recommended_patches of this ComplianceReportTarget.
        :rtype: list[oci.fleet_apps_management.models.ComplianceReportPatchDetail]
        """
        return self._recommended_patches

    @recommended_patches.setter
    def recommended_patches(self, recommended_patches):
        """
        Sets the recommended_patches of this ComplianceReportTarget.
        Recommended Patches for the Target.


        :param recommended_patches: The recommended_patches of this ComplianceReportTarget.
        :type: list[oci.fleet_apps_management.models.ComplianceReportPatchDetail]
        """
        self._recommended_patches = recommended_patches

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
