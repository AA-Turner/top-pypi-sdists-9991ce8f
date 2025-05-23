# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20160918


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VolumeGroupSourceDetails(object):
    """
    Specifies the source for a volume group.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new VolumeGroupSourceDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.core.models.VolumeGroupSourceFromVolumeGroupReplicaDetails`
        * :class:`~oci.core.models.VolumeGroupSourceFromVolumeGroupDetails`
        * :class:`~oci.core.models.VolumeGroupSourceFromVolumesDetails`
        * :class:`~oci.core.models.VolumeGroupSourceFromVolumeGroupBackupDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this VolumeGroupSourceDetails.
        :type type: str

        """
        self.swagger_types = {
            'type': 'str'
        }
        self.attribute_map = {
            'type': 'type'
        }
        self._type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['type']

        if type == 'volumeGroupReplicaId':
            return 'VolumeGroupSourceFromVolumeGroupReplicaDetails'

        if type == 'volumeGroupId':
            return 'VolumeGroupSourceFromVolumeGroupDetails'

        if type == 'volumeIds':
            return 'VolumeGroupSourceFromVolumesDetails'

        if type == 'volumeGroupBackupId':
            return 'VolumeGroupSourceFromVolumeGroupBackupDetails'
        else:
            return 'VolumeGroupSourceDetails'

    @property
    def type(self):
        """
        **[Required]** Gets the type of this VolumeGroupSourceDetails.

        :return: The type of this VolumeGroupSourceDetails.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this VolumeGroupSourceDetails.

        :param type: The type of this VolumeGroupSourceDetails.
        :type: str
        """
        self._type = type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
