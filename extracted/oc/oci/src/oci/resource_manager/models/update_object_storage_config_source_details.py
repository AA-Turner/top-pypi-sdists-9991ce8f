# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20180917

from .update_config_source_details import UpdateConfigSourceDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateObjectStorageConfigSourceDetails(UpdateConfigSourceDetails):
    """
    Update details for an Object Storage bucket that contains Terraform configuration files.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateObjectStorageConfigSourceDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.resource_manager.models.UpdateObjectStorageConfigSourceDetails.config_source_type` attribute
        of this class is ``OBJECT_STORAGE_CONFIG_SOURCE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param config_source_type:
            The value to assign to the config_source_type property of this UpdateObjectStorageConfigSourceDetails.
        :type config_source_type: str

        :param working_directory:
            The value to assign to the working_directory property of this UpdateObjectStorageConfigSourceDetails.
        :type working_directory: str

        :param region:
            The value to assign to the region property of this UpdateObjectStorageConfigSourceDetails.
        :type region: str

        :param namespace:
            The value to assign to the namespace property of this UpdateObjectStorageConfigSourceDetails.
        :type namespace: str

        :param bucket_name:
            The value to assign to the bucket_name property of this UpdateObjectStorageConfigSourceDetails.
        :type bucket_name: str

        """
        self.swagger_types = {
            'config_source_type': 'str',
            'working_directory': 'str',
            'region': 'str',
            'namespace': 'str',
            'bucket_name': 'str'
        }
        self.attribute_map = {
            'config_source_type': 'configSourceType',
            'working_directory': 'workingDirectory',
            'region': 'region',
            'namespace': 'namespace',
            'bucket_name': 'bucketName'
        }
        self._config_source_type = None
        self._working_directory = None
        self._region = None
        self._namespace = None
        self._bucket_name = None
        self._config_source_type = 'OBJECT_STORAGE_CONFIG_SOURCE'

    @property
    def region(self):
        """
        Gets the region of this UpdateObjectStorageConfigSourceDetails.
        The name of the bucket's region.
        Example: `us-phoenix-1`


        :return: The region of this UpdateObjectStorageConfigSourceDetails.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """
        Sets the region of this UpdateObjectStorageConfigSourceDetails.
        The name of the bucket's region.
        Example: `us-phoenix-1`


        :param region: The region of this UpdateObjectStorageConfigSourceDetails.
        :type: str
        """
        self._region = region

    @property
    def namespace(self):
        """
        Gets the namespace of this UpdateObjectStorageConfigSourceDetails.
        The Object Storage namespace that contains the bucket.


        :return: The namespace of this UpdateObjectStorageConfigSourceDetails.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """
        Sets the namespace of this UpdateObjectStorageConfigSourceDetails.
        The Object Storage namespace that contains the bucket.


        :param namespace: The namespace of this UpdateObjectStorageConfigSourceDetails.
        :type: str
        """
        self._namespace = namespace

    @property
    def bucket_name(self):
        """
        Gets the bucket_name of this UpdateObjectStorageConfigSourceDetails.
        The name of the bucket that contains the Terraform configuration files.


        :return: The bucket_name of this UpdateObjectStorageConfigSourceDetails.
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """
        Sets the bucket_name of this UpdateObjectStorageConfigSourceDetails.
        The name of the bucket that contains the Terraform configuration files.


        :param bucket_name: The bucket_name of this UpdateObjectStorageConfigSourceDetails.
        :type: str
        """
        self._bucket_name = bucket_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
