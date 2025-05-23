# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20201101

from .external_database_feature_details import ExternalDatabaseFeatureDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalDatabaseDiagnosticsAndManagementFeatureDetails(ExternalDatabaseFeatureDetails):
    """
    The details required to enable the Diagnostics and Management feature.
    """

    #: A constant which can be used with the license_model property of a ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
    #: This constant has a value of "LICENSE_INCLUDED"
    LICENSE_MODEL_LICENSE_INCLUDED = "LICENSE_INCLUDED"

    #: A constant which can be used with the license_model property of a ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
    #: This constant has a value of "BRING_YOUR_OWN_LICENSE"
    LICENSE_MODEL_BRING_YOUR_OWN_LICENSE = "BRING_YOUR_OWN_LICENSE"

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalDatabaseDiagnosticsAndManagementFeatureDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.database_management.models.ExternalDatabaseDiagnosticsAndManagementFeatureDetails.feature` attribute
        of this class is ``DIAGNOSTICS_AND_MANAGEMENT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param feature:
            The value to assign to the feature property of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
            Allowed values for this property are: "DIAGNOSTICS_AND_MANAGEMENT", "DB_LIFECYCLE_MANAGEMENT", "SQLWATCH"
        :type feature: str

        :param connector_details:
            The value to assign to the connector_details property of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        :type connector_details: oci.database_management.models.ConnectorDetails

        :param license_model:
            The value to assign to the license_model property of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
            Allowed values for this property are: "LICENSE_INCLUDED", "BRING_YOUR_OWN_LICENSE"
        :type license_model: str

        :param can_enable_all_current_pdbs:
            The value to assign to the can_enable_all_current_pdbs property of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        :type can_enable_all_current_pdbs: bool

        :param is_auto_enable_pluggable_database:
            The value to assign to the is_auto_enable_pluggable_database property of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        :type is_auto_enable_pluggable_database: bool

        """
        self.swagger_types = {
            'feature': 'str',
            'connector_details': 'ConnectorDetails',
            'license_model': 'str',
            'can_enable_all_current_pdbs': 'bool',
            'is_auto_enable_pluggable_database': 'bool'
        }
        self.attribute_map = {
            'feature': 'feature',
            'connector_details': 'connectorDetails',
            'license_model': 'licenseModel',
            'can_enable_all_current_pdbs': 'canEnableAllCurrentPdbs',
            'is_auto_enable_pluggable_database': 'isAutoEnablePluggableDatabase'
        }
        self._feature = None
        self._connector_details = None
        self._license_model = None
        self._can_enable_all_current_pdbs = None
        self._is_auto_enable_pluggable_database = None
        self._feature = 'DIAGNOSTICS_AND_MANAGEMENT'

    @property
    def license_model(self):
        """
        **[Required]** Gets the license_model of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        The Oracle license model that applies to the external database.

        Allowed values for this property are: "LICENSE_INCLUDED", "BRING_YOUR_OWN_LICENSE"


        :return: The license_model of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        :rtype: str
        """
        return self._license_model

    @license_model.setter
    def license_model(self, license_model):
        """
        Sets the license_model of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        The Oracle license model that applies to the external database.


        :param license_model: The license_model of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        :type: str
        """
        allowed_values = ["LICENSE_INCLUDED", "BRING_YOUR_OWN_LICENSE"]
        if not value_allowed_none_or_none_sentinel(license_model, allowed_values):
            raise ValueError(
                f"Invalid value for `license_model`, must be None or one of {allowed_values}"
            )
        self._license_model = license_model

    @property
    def can_enable_all_current_pdbs(self):
        """
        Gets the can_enable_all_current_pdbs of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        Indicates whether Diagnostics & Management should be enabled for all the current pluggable databases in the container database.


        :return: The can_enable_all_current_pdbs of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        :rtype: bool
        """
        return self._can_enable_all_current_pdbs

    @can_enable_all_current_pdbs.setter
    def can_enable_all_current_pdbs(self, can_enable_all_current_pdbs):
        """
        Sets the can_enable_all_current_pdbs of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        Indicates whether Diagnostics & Management should be enabled for all the current pluggable databases in the container database.


        :param can_enable_all_current_pdbs: The can_enable_all_current_pdbs of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        :type: bool
        """
        self._can_enable_all_current_pdbs = can_enable_all_current_pdbs

    @property
    def is_auto_enable_pluggable_database(self):
        """
        Gets the is_auto_enable_pluggable_database of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        Indicates whether Diagnostics & Management should be enabled automatically for all the pluggable databases in the container database.


        :return: The is_auto_enable_pluggable_database of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        :rtype: bool
        """
        return self._is_auto_enable_pluggable_database

    @is_auto_enable_pluggable_database.setter
    def is_auto_enable_pluggable_database(self, is_auto_enable_pluggable_database):
        """
        Sets the is_auto_enable_pluggable_database of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        Indicates whether Diagnostics & Management should be enabled automatically for all the pluggable databases in the container database.


        :param is_auto_enable_pluggable_database: The is_auto_enable_pluggable_database of this ExternalDatabaseDiagnosticsAndManagementFeatureDetails.
        :type: bool
        """
        self._is_auto_enable_pluggable_database = is_auto_enable_pluggable_database

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
