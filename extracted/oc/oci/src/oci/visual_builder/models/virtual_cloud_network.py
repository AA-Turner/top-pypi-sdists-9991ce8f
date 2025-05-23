# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20210601


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VirtualCloudNetwork(object):
    """
    Virtual Cloud Network definition.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new VirtualCloudNetwork object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this VirtualCloudNetwork.
        :type id: str

        :param allowlisted_ip_cidrs:
            The value to assign to the allowlisted_ip_cidrs property of this VirtualCloudNetwork.
        :type allowlisted_ip_cidrs: list[str]

        """
        self.swagger_types = {
            'id': 'str',
            'allowlisted_ip_cidrs': 'list[str]'
        }
        self.attribute_map = {
            'id': 'id',
            'allowlisted_ip_cidrs': 'allowlistedIpCidrs'
        }
        self._id = None
        self._allowlisted_ip_cidrs = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this VirtualCloudNetwork.
        The Virtual Cloud Network OCID.


        :return: The id of this VirtualCloudNetwork.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this VirtualCloudNetwork.
        The Virtual Cloud Network OCID.


        :param id: The id of this VirtualCloudNetwork.
        :type: str
        """
        self._id = id

    @property
    def allowlisted_ip_cidrs(self):
        """
        Gets the allowlisted_ip_cidrs of this VirtualCloudNetwork.
        Source IP addresses or IP address ranges ingress rules. (ex: \"168.122.59.5/32\", \"10.20.30.0/26\")
        An invalid IP or CIDR block will result in a 400 response.


        :return: The allowlisted_ip_cidrs of this VirtualCloudNetwork.
        :rtype: list[str]
        """
        return self._allowlisted_ip_cidrs

    @allowlisted_ip_cidrs.setter
    def allowlisted_ip_cidrs(self, allowlisted_ip_cidrs):
        """
        Sets the allowlisted_ip_cidrs of this VirtualCloudNetwork.
        Source IP addresses or IP address ranges ingress rules. (ex: \"168.122.59.5/32\", \"10.20.30.0/26\")
        An invalid IP or CIDR block will result in a 400 response.


        :param allowlisted_ip_cidrs: The allowlisted_ip_cidrs of this VirtualCloudNetwork.
        :type: list[str]
        """
        self._allowlisted_ip_cidrs = allowlisted_ip_cidrs

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
