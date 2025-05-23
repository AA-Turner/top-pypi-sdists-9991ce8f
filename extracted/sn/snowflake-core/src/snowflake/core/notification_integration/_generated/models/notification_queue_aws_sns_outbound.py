# coding: utf-8
"""
    Snowflake Notification Integration API.

    The Snowflake Notification Integration API is a REST API that you can use to access, update, and perform certain actions on Notification Integration resource in a Snowflake database.  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Contact: support@snowflake.com
    Generated by: https://openapi-generator.tech

    Do not edit this file manually.
"""

from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from typing import Union

from snowflake.core.notification_integration._generated.models.notification_hook import NotificationHook

from pydantic import ConfigDict, StrictStr

from typing import Any, ClassVar, Dict, List, Optional


class NotificationQueueAwsSnsOutbound(NotificationHook):
    """A model object representing the NotificationQueueAwsSnsOutbound resource.

    Constructs an object of type NotificationQueueAwsSnsOutbound with the provided properties.

    Parameters
    __________
    aws_sns_topic_arn : str, optional
        Amazon Resource Name (ARN) of the Amazon SNS (SNS) topic to which notifications are pushed.
    aws_sns_role_arn : str, optional
        ARN of the IAM role that has permissions to publish messages to the SNS topic.
    sf_aws_iam_user_arn : str, optional
        ARN for the Snowflake IAM user created for your account.
    sf_aws_external_id : str, optional
        External ID for the Snowflake IAM user created for your account.
    """

    aws_sns_topic_arn: Optional[StrictStr] = None

    aws_sns_role_arn: Optional[StrictStr] = None

    sf_aws_iam_user_arn: Optional[StrictStr] = None

    sf_aws_external_id: Optional[StrictStr] = None

    __properties = ["type"]

    class Config:
        populate_by_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias."""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> NotificationQueueAwsSnsOutbound:
        """Create an instance of NotificationQueueAwsSnsOutbound from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    def to_dict(
        self,
        hide_readonly_properties: bool = False,
    ) -> dict[str, Any]:
        """Returns the dictionary representation of the model using alias."""

        exclude_properties = set()

        if hide_readonly_properties:
            exclude_properties.update({
                "sf_aws_iam_user_arn",
                "sf_aws_external_id",
            })

        _dict = dict(
            self._iter(to_dict=True,
                       by_alias=True,
                       exclude=exclude_properties,
                       exclude_none=True))

        _dict['type'] = NotificationHook.get_child_model_discriminator_value(
            'NotificationQueueAwsSnsOutbound')

        return _dict

    def to_dict_without_readonly_properties(self) -> dict[str, Any]:
        """Return the dictionary representation of the model without readonly properties."""
        return self.to_dict(hide_readonly_properties=True)

    @classmethod
    def from_dict(cls, obj: dict) -> NotificationQueueAwsSnsOutbound:
        """Create an instance of NotificationQueueAwsSnsOutbound from a dict."""

        if obj is None:
            return None

        if type(obj) is not dict:
            return NotificationQueueAwsSnsOutbound.parse_obj(obj)

        _obj = NotificationQueueAwsSnsOutbound.parse_obj({
            "aws_sns_topic_arn":
            obj.get("aws_sns_topic_arn"),
            "aws_sns_role_arn":
            obj.get("aws_sns_role_arn"),
            "sf_aws_iam_user_arn":
            obj.get("sf_aws_iam_user_arn"),
            "sf_aws_external_id":
            obj.get("sf_aws_external_id"),
        })

        return _obj


from typing import Optional, List, Dict

from snowflake.core.notification_integration._generated.models.notification_hook import NotificationHook


class NotificationQueueAwsSnsOutboundModel(NotificationHook):

    def __init__(
        self,  # optional properties
        aws_sns_topic_arn: Optional[str] = None,
        aws_sns_role_arn: Optional[str] = None,
        sf_aws_iam_user_arn: Optional[str] = None,
        sf_aws_external_id: Optional[str] = None,
    ):
        """A model object representing the NotificationQueueAwsSnsOutbound resource.

        Constructs an object of type NotificationQueueAwsSnsOutbound with the provided properties.

        Parameters
        __________
        aws_sns_topic_arn : str, optional
            Amazon Resource Name (ARN) of the Amazon SNS (SNS) topic to which notifications are pushed.
        aws_sns_role_arn : str, optional
            ARN of the IAM role that has permissions to publish messages to the SNS topic.
        sf_aws_iam_user_arn : str, optional
            ARN for the Snowflake IAM user created for your account.
        sf_aws_external_id : str, optional
            External ID for the Snowflake IAM user created for your account.
        """

        super().__init__()
        self.aws_sns_topic_arn = aws_sns_topic_arn
        self.aws_sns_role_arn = aws_sns_role_arn
        self.sf_aws_iam_user_arn = sf_aws_iam_user_arn
        self.sf_aws_external_id = sf_aws_external_id

    __properties = ["type"]

    def __repr__(self) -> str:
        return repr(self._to_model())

    def _to_model(self):
        return NotificationQueueAwsSnsOutbound(
            aws_sns_topic_arn=self.aws_sns_topic_arn,
            aws_sns_role_arn=self.aws_sns_role_arn,
            sf_aws_iam_user_arn=self.sf_aws_iam_user_arn,
            sf_aws_external_id=self.sf_aws_external_id,
        )

    @classmethod
    def _from_model(cls, model) -> NotificationQueueAwsSnsOutboundModel:
        return NotificationQueueAwsSnsOutboundModel(
            aws_sns_topic_arn=model.aws_sns_topic_arn,
            aws_sns_role_arn=model.aws_sns_role_arn,
            sf_aws_iam_user_arn=model.sf_aws_iam_user_arn,
            sf_aws_external_id=model.sf_aws_external_id,
        )

    def to_dict(self):
        """Creates a dictionary of the properties from a NotificationQueueAwsSnsOutbound.

        This method constructs a dictionary with the key-value entries corresponding to the properties of the NotificationQueueAwsSnsOutbound object.

        Returns
        _______
        dict
            A dictionary object created using the input model.
        """
        return self._to_model().to_dict()

    @classmethod
    def from_dict(cls, obj: dict) -> NotificationQueueAwsSnsOutboundModel:
        """Creates an instance of NotificationQueueAwsSnsOutbound from a dict.

        This method constructs a NotificationQueueAwsSnsOutbound object from a dictionary with the key-value pairs of its properties.

        Parameters
        ----------
        obj : dict
            A dictionary whose keys and values correspond to the properties of the resource object.

        Returns
        _______
        NotificationQueueAwsSnsOutbound
            A NotificationQueueAwsSnsOutbound object created using the input dictionary; this will fail if the required properties are missing.
        """
        return cls._from_model(NotificationQueueAwsSnsOutbound.from_dict(obj))


NotificationQueueAwsSnsOutbound._model_class = NotificationQueueAwsSnsOutboundModel
