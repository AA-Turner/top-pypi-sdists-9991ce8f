# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20211001


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class InitialImportDatasetConfiguration(object):
    """
    Initial import dataset configuration. Allows user to create dataset from existing dataset files.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new InitialImportDatasetConfiguration object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param import_format:
            The value to assign to the import_format property of this InitialImportDatasetConfiguration.
        :type import_format: oci.data_labeling_service.models.ImportFormat

        :param import_metadata_path:
            The value to assign to the import_metadata_path property of this InitialImportDatasetConfiguration.
        :type import_metadata_path: oci.data_labeling_service.models.ImportMetadataPath

        """
        self.swagger_types = {
            'import_format': 'ImportFormat',
            'import_metadata_path': 'ImportMetadataPath'
        }
        self.attribute_map = {
            'import_format': 'importFormat',
            'import_metadata_path': 'importMetadataPath'
        }
        self._import_format = None
        self._import_metadata_path = None

    @property
    def import_format(self):
        """
        **[Required]** Gets the import_format of this InitialImportDatasetConfiguration.

        :return: The import_format of this InitialImportDatasetConfiguration.
        :rtype: oci.data_labeling_service.models.ImportFormat
        """
        return self._import_format

    @import_format.setter
    def import_format(self, import_format):
        """
        Sets the import_format of this InitialImportDatasetConfiguration.

        :param import_format: The import_format of this InitialImportDatasetConfiguration.
        :type: oci.data_labeling_service.models.ImportFormat
        """
        self._import_format = import_format

    @property
    def import_metadata_path(self):
        """
        **[Required]** Gets the import_metadata_path of this InitialImportDatasetConfiguration.

        :return: The import_metadata_path of this InitialImportDatasetConfiguration.
        :rtype: oci.data_labeling_service.models.ImportMetadataPath
        """
        return self._import_metadata_path

    @import_metadata_path.setter
    def import_metadata_path(self, import_metadata_path):
        """
        Sets the import_metadata_path of this InitialImportDatasetConfiguration.

        :param import_metadata_path: The import_metadata_path of this InitialImportDatasetConfiguration.
        :type: oci.data_labeling_service.models.ImportMetadataPath
        """
        self._import_metadata_path = import_metadata_path

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
