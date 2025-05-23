# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20180828


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ShapesDetails(object):
    """
    Shapes for OpenSearch Cluster.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ShapesDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param shapes:
            The value to assign to the shapes property of this ShapesDetails.
        :type shapes: list[str]

        """
        self.swagger_types = {
            'shapes': 'list[str]'
        }
        self.attribute_map = {
            'shapes': 'shapes'
        }
        self._shapes = None

    @property
    def shapes(self):
        """
        Gets the shapes of this ShapesDetails.
        List of Shapes.


        :return: The shapes of this ShapesDetails.
        :rtype: list[str]
        """
        return self._shapes

    @shapes.setter
    def shapes(self, shapes):
        """
        Sets the shapes of this ShapesDetails.
        List of Shapes.


        :param shapes: The shapes of this ShapesDetails.
        :type: list[str]
        """
        self._shapes = shapes

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
