# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220915


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Configuration(object):
    """
    PostgreSQL configuration for a database system.
    """

    #: A constant which can be used with the lifecycle_state property of a Configuration.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a Configuration.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a Configuration.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a Configuration.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the config_type property of a Configuration.
    #: This constant has a value of "DEFAULT"
    CONFIG_TYPE_DEFAULT = "DEFAULT"

    #: A constant which can be used with the config_type property of a Configuration.
    #: This constant has a value of "CUSTOM"
    CONFIG_TYPE_CUSTOM = "CUSTOM"

    #: A constant which can be used with the config_type property of a Configuration.
    #: This constant has a value of "COPIED"
    CONFIG_TYPE_COPIED = "COPIED"

    def __init__(self, **kwargs):
        """
        Initializes a new Configuration object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this Configuration.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this Configuration.
        :type display_name: str

        :param description:
            The value to assign to the description property of this Configuration.
        :type description: str

        :param compartment_id:
            The value to assign to the compartment_id property of this Configuration.
        :type compartment_id: str

        :param time_created:
            The value to assign to the time_created property of this Configuration.
        :type time_created: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this Configuration.
            Allowed values for this property are: "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this Configuration.
        :type lifecycle_details: str

        :param db_version:
            The value to assign to the db_version property of this Configuration.
        :type db_version: str

        :param config_type:
            The value to assign to the config_type property of this Configuration.
            Allowed values for this property are: "DEFAULT", "CUSTOM", "COPIED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type config_type: str

        :param shape:
            The value to assign to the shape property of this Configuration.
        :type shape: str

        :param is_flexible:
            The value to assign to the is_flexible property of this Configuration.
        :type is_flexible: bool

        :param instance_ocpu_count:
            The value to assign to the instance_ocpu_count property of this Configuration.
        :type instance_ocpu_count: int

        :param instance_memory_size_in_gbs:
            The value to assign to the instance_memory_size_in_gbs property of this Configuration.
        :type instance_memory_size_in_gbs: int

        :param configuration_details:
            The value to assign to the configuration_details property of this Configuration.
        :type configuration_details: oci.psql.models.ConfigurationDetails

        :param freeform_tags:
            The value to assign to the freeform_tags property of this Configuration.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this Configuration.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this Configuration.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'description': 'str',
            'compartment_id': 'str',
            'time_created': 'datetime',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'db_version': 'str',
            'config_type': 'str',
            'shape': 'str',
            'is_flexible': 'bool',
            'instance_ocpu_count': 'int',
            'instance_memory_size_in_gbs': 'int',
            'configuration_details': 'ConfigurationDetails',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }
        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'description': 'description',
            'compartment_id': 'compartmentId',
            'time_created': 'timeCreated',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'db_version': 'dbVersion',
            'config_type': 'configType',
            'shape': 'shape',
            'is_flexible': 'isFlexible',
            'instance_ocpu_count': 'instanceOcpuCount',
            'instance_memory_size_in_gbs': 'instanceMemorySizeInGBs',
            'configuration_details': 'configurationDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }
        self._id = None
        self._display_name = None
        self._description = None
        self._compartment_id = None
        self._time_created = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._db_version = None
        self._config_type = None
        self._shape = None
        self._is_flexible = None
        self._instance_ocpu_count = None
        self._instance_memory_size_in_gbs = None
        self._configuration_details = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this Configuration.
        A unique identifier for the configuration. Immutable on creation.


        :return: The id of this Configuration.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Configuration.
        A unique identifier for the configuration. Immutable on creation.


        :param id: The id of this Configuration.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this Configuration.
        A user-friendly display name for the configuration. Avoid entering confidential information.


        :return: The display_name of this Configuration.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this Configuration.
        A user-friendly display name for the configuration. Avoid entering confidential information.


        :param display_name: The display_name of this Configuration.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this Configuration.
        A description for the configuration.


        :return: The description of this Configuration.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this Configuration.
        A description for the configuration.


        :param description: The description of this Configuration.
        :type: str
        """
        self._description = description

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this Configuration.
        The `OCID`__ of the compartment that contains the configuration.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this Configuration.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this Configuration.
        The `OCID`__ of the compartment that contains the configuration.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this Configuration.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this Configuration.
        The date and time that the configuration was created, expressed in
        `RFC 3339`__ timestamp format.

        Example: `2016-08-25T21:10:29.600Z`

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_created of this Configuration.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this Configuration.
        The date and time that the configuration was created, expressed in
        `RFC 3339`__ timestamp format.

        Example: `2016-08-25T21:10:29.600Z`

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_created: The time_created of this Configuration.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this Configuration.
        The current state of the configuration.

        Allowed values for this property are: "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this Configuration.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this Configuration.
        The current state of the configuration.


        :param lifecycle_state: The lifecycle_state of this Configuration.
        :type: str
        """
        allowed_values = ["ACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this Configuration.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :return: The lifecycle_details of this Configuration.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this Configuration.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :param lifecycle_details: The lifecycle_details of this Configuration.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def db_version(self):
        """
        **[Required]** Gets the db_version of this Configuration.
        Version of the PostgreSQL database.


        :return: The db_version of this Configuration.
        :rtype: str
        """
        return self._db_version

    @db_version.setter
    def db_version(self, db_version):
        """
        Sets the db_version of this Configuration.
        Version of the PostgreSQL database.


        :param db_version: The db_version of this Configuration.
        :type: str
        """
        self._db_version = db_version

    @property
    def config_type(self):
        """
        Gets the config_type of this Configuration.
        The type of configuration. Either user-created or a default configuration.

        Allowed values for this property are: "DEFAULT", "CUSTOM", "COPIED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The config_type of this Configuration.
        :rtype: str
        """
        return self._config_type

    @config_type.setter
    def config_type(self, config_type):
        """
        Sets the config_type of this Configuration.
        The type of configuration. Either user-created or a default configuration.


        :param config_type: The config_type of this Configuration.
        :type: str
        """
        allowed_values = ["DEFAULT", "CUSTOM", "COPIED"]
        if not value_allowed_none_or_none_sentinel(config_type, allowed_values):
            config_type = 'UNKNOWN_ENUM_VALUE'
        self._config_type = config_type

    @property
    def shape(self):
        """
        **[Required]** Gets the shape of this Configuration.
        The name of the shape for the configuration.
        Example: `VM.Standard.E4.Flex`


        :return: The shape of this Configuration.
        :rtype: str
        """
        return self._shape

    @shape.setter
    def shape(self, shape):
        """
        Sets the shape of this Configuration.
        The name of the shape for the configuration.
        Example: `VM.Standard.E4.Flex`


        :param shape: The shape of this Configuration.
        :type: str
        """
        self._shape = shape

    @property
    def is_flexible(self):
        """
        Gets the is_flexible of this Configuration.
        Whether the configuration supports flexible shapes.


        :return: The is_flexible of this Configuration.
        :rtype: bool
        """
        return self._is_flexible

    @is_flexible.setter
    def is_flexible(self, is_flexible):
        """
        Sets the is_flexible of this Configuration.
        Whether the configuration supports flexible shapes.


        :param is_flexible: The is_flexible of this Configuration.
        :type: bool
        """
        self._is_flexible = is_flexible

    @property
    def instance_ocpu_count(self):
        """
        **[Required]** Gets the instance_ocpu_count of this Configuration.
        CPU core count.

        It's value is set to 0 if configuration is for a flexible shape.


        :return: The instance_ocpu_count of this Configuration.
        :rtype: int
        """
        return self._instance_ocpu_count

    @instance_ocpu_count.setter
    def instance_ocpu_count(self, instance_ocpu_count):
        """
        Sets the instance_ocpu_count of this Configuration.
        CPU core count.

        It's value is set to 0 if configuration is for a flexible shape.


        :param instance_ocpu_count: The instance_ocpu_count of this Configuration.
        :type: int
        """
        self._instance_ocpu_count = instance_ocpu_count

    @property
    def instance_memory_size_in_gbs(self):
        """
        **[Required]** Gets the instance_memory_size_in_gbs of this Configuration.
        Memory size in gigabytes with 1GB increment.

        It's value is set to 0 if configuration is for a flexible shape.


        :return: The instance_memory_size_in_gbs of this Configuration.
        :rtype: int
        """
        return self._instance_memory_size_in_gbs

    @instance_memory_size_in_gbs.setter
    def instance_memory_size_in_gbs(self, instance_memory_size_in_gbs):
        """
        Sets the instance_memory_size_in_gbs of this Configuration.
        Memory size in gigabytes with 1GB increment.

        It's value is set to 0 if configuration is for a flexible shape.


        :param instance_memory_size_in_gbs: The instance_memory_size_in_gbs of this Configuration.
        :type: int
        """
        self._instance_memory_size_in_gbs = instance_memory_size_in_gbs

    @property
    def configuration_details(self):
        """
        **[Required]** Gets the configuration_details of this Configuration.

        :return: The configuration_details of this Configuration.
        :rtype: oci.psql.models.ConfigurationDetails
        """
        return self._configuration_details

    @configuration_details.setter
    def configuration_details(self, configuration_details):
        """
        Sets the configuration_details of this Configuration.

        :param configuration_details: The configuration_details of this Configuration.
        :type: oci.psql.models.ConfigurationDetails
        """
        self._configuration_details = configuration_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this Configuration.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this Configuration.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this Configuration.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this Configuration.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this Configuration.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this Configuration.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this Configuration.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this Configuration.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this Configuration.
        System tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this Configuration.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this Configuration.
        System tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this Configuration.
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
