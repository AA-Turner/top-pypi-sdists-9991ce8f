# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20230801


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DelegationControl(object):
    """
    Delegation Control enables you to grant, audit, or revoke the access Oracle has to your Exadata Cloud infrastructure, and obtain audit reports of all actions taken by a human operator, in a near real-time manner.
    """

    #: A constant which can be used with the resource_type property of a DelegationControl.
    #: This constant has a value of "VMCLUSTER"
    RESOURCE_TYPE_VMCLUSTER = "VMCLUSTER"

    #: A constant which can be used with the resource_type property of a DelegationControl.
    #: This constant has a value of "CLOUDVMCLUSTER"
    RESOURCE_TYPE_CLOUDVMCLUSTER = "CLOUDVMCLUSTER"

    #: A constant which can be used with the notification_message_format property of a DelegationControl.
    #: This constant has a value of "JSON"
    NOTIFICATION_MESSAGE_FORMAT_JSON = "JSON"

    #: A constant which can be used with the notification_message_format property of a DelegationControl.
    #: This constant has a value of "HTML"
    NOTIFICATION_MESSAGE_FORMAT_HTML = "HTML"

    #: A constant which can be used with the lifecycle_state property of a DelegationControl.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a DelegationControl.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a DelegationControl.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a DelegationControl.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a DelegationControl.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a DelegationControl.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a DelegationControl.
    #: This constant has a value of "NEEDS_ATTENTION"
    LIFECYCLE_STATE_NEEDS_ATTENTION = "NEEDS_ATTENTION"

    def __init__(self, **kwargs):
        """
        Initializes a new DelegationControl object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DelegationControl.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this DelegationControl.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this DelegationControl.
        :type display_name: str

        :param description:
            The value to assign to the description property of this DelegationControl.
        :type description: str

        :param num_approvals_required:
            The value to assign to the num_approvals_required property of this DelegationControl.
        :type num_approvals_required: int

        :param pre_approved_service_provider_action_names:
            The value to assign to the pre_approved_service_provider_action_names property of this DelegationControl.
        :type pre_approved_service_provider_action_names: list[str]

        :param delegation_subscription_ids:
            The value to assign to the delegation_subscription_ids property of this DelegationControl.
        :type delegation_subscription_ids: list[str]

        :param is_auto_approve_during_maintenance:
            The value to assign to the is_auto_approve_during_maintenance property of this DelegationControl.
        :type is_auto_approve_during_maintenance: bool

        :param resource_ids:
            The value to assign to the resource_ids property of this DelegationControl.
        :type resource_ids: list[str]

        :param resource_type:
            The value to assign to the resource_type property of this DelegationControl.
            Allowed values for this property are: "VMCLUSTER", "CLOUDVMCLUSTER", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type resource_type: str

        :param notification_topic_id:
            The value to assign to the notification_topic_id property of this DelegationControl.
        :type notification_topic_id: str

        :param notification_message_format:
            The value to assign to the notification_message_format property of this DelegationControl.
            Allowed values for this property are: "JSON", "HTML", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type notification_message_format: str

        :param vault_id:
            The value to assign to the vault_id property of this DelegationControl.
        :type vault_id: str

        :param vault_key_id:
            The value to assign to the vault_key_id property of this DelegationControl.
        :type vault_key_id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this DelegationControl.
            Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_state_details:
            The value to assign to the lifecycle_state_details property of this DelegationControl.
        :type lifecycle_state_details: str

        :param time_created:
            The value to assign to the time_created property of this DelegationControl.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this DelegationControl.
        :type time_updated: datetime

        :param time_deleted:
            The value to assign to the time_deleted property of this DelegationControl.
        :type time_deleted: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this DelegationControl.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this DelegationControl.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this DelegationControl.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'num_approvals_required': 'int',
            'pre_approved_service_provider_action_names': 'list[str]',
            'delegation_subscription_ids': 'list[str]',
            'is_auto_approve_during_maintenance': 'bool',
            'resource_ids': 'list[str]',
            'resource_type': 'str',
            'notification_topic_id': 'str',
            'notification_message_format': 'str',
            'vault_id': 'str',
            'vault_key_id': 'str',
            'lifecycle_state': 'str',
            'lifecycle_state_details': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'time_deleted': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }
        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'description': 'description',
            'num_approvals_required': 'numApprovalsRequired',
            'pre_approved_service_provider_action_names': 'preApprovedServiceProviderActionNames',
            'delegation_subscription_ids': 'delegationSubscriptionIds',
            'is_auto_approve_during_maintenance': 'isAutoApproveDuringMaintenance',
            'resource_ids': 'resourceIds',
            'resource_type': 'resourceType',
            'notification_topic_id': 'notificationTopicId',
            'notification_message_format': 'notificationMessageFormat',
            'vault_id': 'vaultId',
            'vault_key_id': 'vaultKeyId',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_state_details': 'lifecycleStateDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'time_deleted': 'timeDeleted',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }
        self._id = None
        self._compartment_id = None
        self._display_name = None
        self._description = None
        self._num_approvals_required = None
        self._pre_approved_service_provider_action_names = None
        self._delegation_subscription_ids = None
        self._is_auto_approve_during_maintenance = None
        self._resource_ids = None
        self._resource_type = None
        self._notification_topic_id = None
        self._notification_message_format = None
        self._vault_id = None
        self._vault_key_id = None
        self._lifecycle_state = None
        self._lifecycle_state_details = None
        self._time_created = None
        self._time_updated = None
        self._time_deleted = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this DelegationControl.
        The OCID of the Delegation Control.


        :return: The id of this DelegationControl.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DelegationControl.
        The OCID of the Delegation Control.


        :param id: The id of this DelegationControl.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this DelegationControl.
        The OCID of the compartment that contains the Delegation Control.


        :return: The compartment_id of this DelegationControl.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this DelegationControl.
        The OCID of the compartment that contains the Delegation Control.


        :param compartment_id: The compartment_id of this DelegationControl.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this DelegationControl.
        Name of the Delegation Control. The name does not need to be unique.


        :return: The display_name of this DelegationControl.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this DelegationControl.
        Name of the Delegation Control. The name does not need to be unique.


        :param display_name: The display_name of this DelegationControl.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this DelegationControl.
        Description of the Delegation Control.


        :return: The description of this DelegationControl.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this DelegationControl.
        Description of the Delegation Control.


        :param description: The description of this DelegationControl.
        :type: str
        """
        self._description = description

    @property
    def num_approvals_required(self):
        """
        Gets the num_approvals_required of this DelegationControl.
        number of approvals required.


        :return: The num_approvals_required of this DelegationControl.
        :rtype: int
        """
        return self._num_approvals_required

    @num_approvals_required.setter
    def num_approvals_required(self, num_approvals_required):
        """
        Sets the num_approvals_required of this DelegationControl.
        number of approvals required.


        :param num_approvals_required: The num_approvals_required of this DelegationControl.
        :type: int
        """
        self._num_approvals_required = num_approvals_required

    @property
    def pre_approved_service_provider_action_names(self):
        """
        Gets the pre_approved_service_provider_action_names of this DelegationControl.
        List of pre-approved Service Provider Action names. The list of pre-defined Service Provider Actions can be obtained from the ListServiceProviderActions API. Delegated Resource Access Requests associated with a resource governed by this Delegation Control will be
        automatically approved if the Delegated Resource Access Request only contain Service Provider Actions in the pre-approved list.


        :return: The pre_approved_service_provider_action_names of this DelegationControl.
        :rtype: list[str]
        """
        return self._pre_approved_service_provider_action_names

    @pre_approved_service_provider_action_names.setter
    def pre_approved_service_provider_action_names(self, pre_approved_service_provider_action_names):
        """
        Sets the pre_approved_service_provider_action_names of this DelegationControl.
        List of pre-approved Service Provider Action names. The list of pre-defined Service Provider Actions can be obtained from the ListServiceProviderActions API. Delegated Resource Access Requests associated with a resource governed by this Delegation Control will be
        automatically approved if the Delegated Resource Access Request only contain Service Provider Actions in the pre-approved list.


        :param pre_approved_service_provider_action_names: The pre_approved_service_provider_action_names of this DelegationControl.
        :type: list[str]
        """
        self._pre_approved_service_provider_action_names = pre_approved_service_provider_action_names

    @property
    def delegation_subscription_ids(self):
        """
        Gets the delegation_subscription_ids of this DelegationControl.
        List of Delegation Subscription OCID that are allowed for this Delegation Control. The allowed subscriptions will determine the available Service Provider Actions. Only support operators for the allowed subscriptions are allowed to create Delegated Resource Access Request.


        :return: The delegation_subscription_ids of this DelegationControl.
        :rtype: list[str]
        """
        return self._delegation_subscription_ids

    @delegation_subscription_ids.setter
    def delegation_subscription_ids(self, delegation_subscription_ids):
        """
        Sets the delegation_subscription_ids of this DelegationControl.
        List of Delegation Subscription OCID that are allowed for this Delegation Control. The allowed subscriptions will determine the available Service Provider Actions. Only support operators for the allowed subscriptions are allowed to create Delegated Resource Access Request.


        :param delegation_subscription_ids: The delegation_subscription_ids of this DelegationControl.
        :type: list[str]
        """
        self._delegation_subscription_ids = delegation_subscription_ids

    @property
    def is_auto_approve_during_maintenance(self):
        """
        Gets the is_auto_approve_during_maintenance of this DelegationControl.
        Set to true to allow all Delegated Resource Access Request to be approved automatically during maintenance.


        :return: The is_auto_approve_during_maintenance of this DelegationControl.
        :rtype: bool
        """
        return self._is_auto_approve_during_maintenance

    @is_auto_approve_during_maintenance.setter
    def is_auto_approve_during_maintenance(self, is_auto_approve_during_maintenance):
        """
        Sets the is_auto_approve_during_maintenance of this DelegationControl.
        Set to true to allow all Delegated Resource Access Request to be approved automatically during maintenance.


        :param is_auto_approve_during_maintenance: The is_auto_approve_during_maintenance of this DelegationControl.
        :type: bool
        """
        self._is_auto_approve_during_maintenance = is_auto_approve_during_maintenance

    @property
    def resource_ids(self):
        """
        Gets the resource_ids of this DelegationControl.
        The OCID of the selected resources that this Delegation Control is applicable to.


        :return: The resource_ids of this DelegationControl.
        :rtype: list[str]
        """
        return self._resource_ids

    @resource_ids.setter
    def resource_ids(self, resource_ids):
        """
        Sets the resource_ids of this DelegationControl.
        The OCID of the selected resources that this Delegation Control is applicable to.


        :param resource_ids: The resource_ids of this DelegationControl.
        :type: list[str]
        """
        self._resource_ids = resource_ids

    @property
    def resource_type(self):
        """
        **[Required]** Gets the resource_type of this DelegationControl.
        Resource type for which the Delegation Control is applicable to.

        Allowed values for this property are: "VMCLUSTER", "CLOUDVMCLUSTER", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The resource_type of this DelegationControl.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """
        Sets the resource_type of this DelegationControl.
        Resource type for which the Delegation Control is applicable to.


        :param resource_type: The resource_type of this DelegationControl.
        :type: str
        """
        allowed_values = ["VMCLUSTER", "CLOUDVMCLUSTER"]
        if not value_allowed_none_or_none_sentinel(resource_type, allowed_values):
            resource_type = 'UNKNOWN_ENUM_VALUE'
        self._resource_type = resource_type

    @property
    def notification_topic_id(self):
        """
        Gets the notification_topic_id of this DelegationControl.
        The OCID of the OCI Notification topic to publish messages related to this Delegation Control.


        :return: The notification_topic_id of this DelegationControl.
        :rtype: str
        """
        return self._notification_topic_id

    @notification_topic_id.setter
    def notification_topic_id(self, notification_topic_id):
        """
        Sets the notification_topic_id of this DelegationControl.
        The OCID of the OCI Notification topic to publish messages related to this Delegation Control.


        :param notification_topic_id: The notification_topic_id of this DelegationControl.
        :type: str
        """
        self._notification_topic_id = notification_topic_id

    @property
    def notification_message_format(self):
        """
        Gets the notification_message_format of this DelegationControl.
        The format of the OCI Notification messages for this Delegation Control.

        Allowed values for this property are: "JSON", "HTML", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The notification_message_format of this DelegationControl.
        :rtype: str
        """
        return self._notification_message_format

    @notification_message_format.setter
    def notification_message_format(self, notification_message_format):
        """
        Sets the notification_message_format of this DelegationControl.
        The format of the OCI Notification messages for this Delegation Control.


        :param notification_message_format: The notification_message_format of this DelegationControl.
        :type: str
        """
        allowed_values = ["JSON", "HTML"]
        if not value_allowed_none_or_none_sentinel(notification_message_format, allowed_values):
            notification_message_format = 'UNKNOWN_ENUM_VALUE'
        self._notification_message_format = notification_message_format

    @property
    def vault_id(self):
        """
        Gets the vault_id of this DelegationControl.
        The OCID of the OCI Vault that will store the secrets containing the SSH keys to access the resource governed by this Delegation Control by Delegate Access Control Service. This property is required when resourceType is CLOUDVMCLUSTER. Delegate Access Control Service will generate the SSH keys and store them as secrets in the OCI Vault.


        :return: The vault_id of this DelegationControl.
        :rtype: str
        """
        return self._vault_id

    @vault_id.setter
    def vault_id(self, vault_id):
        """
        Sets the vault_id of this DelegationControl.
        The OCID of the OCI Vault that will store the secrets containing the SSH keys to access the resource governed by this Delegation Control by Delegate Access Control Service. This property is required when resourceType is CLOUDVMCLUSTER. Delegate Access Control Service will generate the SSH keys and store them as secrets in the OCI Vault.


        :param vault_id: The vault_id of this DelegationControl.
        :type: str
        """
        self._vault_id = vault_id

    @property
    def vault_key_id(self):
        """
        Gets the vault_key_id of this DelegationControl.
        The OCID of the Master Encryption Key in the OCI Vault specified by vaultId. This key will be used to encrypt the SSH keys to access the resource governed by this Delegation Control by Delegate Access Control Service. This property is required when resourceType is CLOUDVMCLUSTER.


        :return: The vault_key_id of this DelegationControl.
        :rtype: str
        """
        return self._vault_key_id

    @vault_key_id.setter
    def vault_key_id(self, vault_key_id):
        """
        Sets the vault_key_id of this DelegationControl.
        The OCID of the Master Encryption Key in the OCI Vault specified by vaultId. This key will be used to encrypt the SSH keys to access the resource governed by this Delegation Control by Delegate Access Control Service. This property is required when resourceType is CLOUDVMCLUSTER.


        :param vault_key_id: The vault_key_id of this DelegationControl.
        :type: str
        """
        self._vault_key_id = vault_key_id

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this DelegationControl.
        The current lifecycle state of the Delegation Control.

        Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this DelegationControl.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this DelegationControl.
        The current lifecycle state of the Delegation Control.


        :param lifecycle_state: The lifecycle_state of this DelegationControl.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_state_details(self):
        """
        Gets the lifecycle_state_details of this DelegationControl.
        Description of the current lifecycle state in more detail.


        :return: The lifecycle_state_details of this DelegationControl.
        :rtype: str
        """
        return self._lifecycle_state_details

    @lifecycle_state_details.setter
    def lifecycle_state_details(self, lifecycle_state_details):
        """
        Sets the lifecycle_state_details of this DelegationControl.
        Description of the current lifecycle state in more detail.


        :param lifecycle_state_details: The lifecycle_state_details of this DelegationControl.
        :type: str
        """
        self._lifecycle_state_details = lifecycle_state_details

    @property
    def time_created(self):
        """
        Gets the time_created of this DelegationControl.
        Time when the Delegation Control was created expressed in `RFC 3339`__ timestamp format, e.g. '2020-05-22T21:10:29.600Z'

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this DelegationControl.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this DelegationControl.
        Time when the Delegation Control was created expressed in `RFC 3339`__ timestamp format, e.g. '2020-05-22T21:10:29.600Z'

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this DelegationControl.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this DelegationControl.
        Time when the Delegation Control was last modified expressed in `RFC 3339`__ timestamp format, e.g. '2020-05-22T21:10:29.600Z'

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_updated of this DelegationControl.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this DelegationControl.
        Time when the Delegation Control was last modified expressed in `RFC 3339`__ timestamp format, e.g. '2020-05-22T21:10:29.600Z'

        __ https://tools.ietf.org/html/rfc3339


        :param time_updated: The time_updated of this DelegationControl.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def time_deleted(self):
        """
        Gets the time_deleted of this DelegationControl.
        Time when the Delegation Control was deleted expressed in `RFC 3339`__timestamp format, e.g. '2020-05-22T21:10:29.600Z'.
        Note a deleted Delegation Control still stays in the system, so that you can still audit Service Provider Actions associated with Delegated Resource Access Requests
        raised on target resources governed by the deleted Delegation Control.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_deleted of this DelegationControl.
        :rtype: datetime
        """
        return self._time_deleted

    @time_deleted.setter
    def time_deleted(self, time_deleted):
        """
        Sets the time_deleted of this DelegationControl.
        Time when the Delegation Control was deleted expressed in `RFC 3339`__timestamp format, e.g. '2020-05-22T21:10:29.600Z'.
        Note a deleted Delegation Control still stays in the system, so that you can still audit Service Provider Actions associated with Delegated Resource Access Requests
        raised on target resources governed by the deleted Delegation Control.

        __ https://tools.ietf.org/html/rfc3339


        :param time_deleted: The time_deleted of this DelegationControl.
        :type: datetime
        """
        self._time_deleted = time_deleted

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this DelegationControl.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this DelegationControl.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this DelegationControl.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this DelegationControl.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this DelegationControl.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this DelegationControl.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this DelegationControl.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this DelegationControl.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this DelegationControl.
        System tags for this resource. Each key is predefined and scoped to a namespace.

        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this DelegationControl.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this DelegationControl.
        System tags for this resource. Each key is predefined and scoped to a namespace.

        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this DelegationControl.
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
