# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20221001


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PreDeployedLanguageModels(object):
    """
    Description of Language Entities.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PreDeployedLanguageModels object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this PreDeployedLanguageModels.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this PreDeployedLanguageModels.
        :type compartment_id: str

        :param description:
            The value to assign to the description property of this PreDeployedLanguageModels.
        :type description: str

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'description': 'str'
        }
        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'description': 'description'
        }
        self._id = None
        self._compartment_id = None
        self._description = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this PreDeployedLanguageModels.
        Unique identifier that is immutable on creation


        :return: The id of this PreDeployedLanguageModels.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PreDeployedLanguageModels.
        Unique identifier that is immutable on creation


        :param id: The id of this PreDeployedLanguageModels.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this PreDeployedLanguageModels.
        The `OCID`__ Compartment Identifier

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this PreDeployedLanguageModels.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this PreDeployedLanguageModels.
        The `OCID`__ Compartment Identifier

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this PreDeployedLanguageModels.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def description(self):
        """
        Gets the description of this PreDeployedLanguageModels.
        Language Entities Description


        :return: The description of this PreDeployedLanguageModels.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PreDeployedLanguageModels.
        Language Entities Description


        :param description: The description of this PreDeployedLanguageModels.
        :type: str
        """
        self._description = description

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
