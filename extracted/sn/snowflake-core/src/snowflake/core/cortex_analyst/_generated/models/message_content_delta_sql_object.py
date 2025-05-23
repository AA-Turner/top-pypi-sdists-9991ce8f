# coding: utf-8
"""
    Cortex Analyst API.

    The Snowflake Cortex Analyst API is a REST API that allows end user to chat with their data leveraging semantic models to generate SQL queries.  # noqa: E501

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

from snowflake.core.cortex_analyst._generated.models.confidence import Confidence

from snowflake.core.cortex_analyst._generated.models.message_content_delta import MessageContentDelta

from pydantic import ConfigDict, StrictStr

from typing import Any, ClassVar, Dict, List, Optional


class MessageContentDeltaSqlObject(MessageContentDelta):
    """A model object representing the MessageContentDeltaSqlObject resource.

    Constructs an object of type MessageContentDeltaSqlObject with the provided properties.

    Parameters
    __________
    statement_delta : str
        The delta of the sql statement, clients should concatenate all deltas for the same index

    index : int, optional
        The index of the content array this delta object represents

    confidence : Confidence, optional
    """

    statement_delta: StrictStr

    confidence: Optional[Confidence] = None

    __properties = ["type", "index", "statement_delta", "confidence"]

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
    def from_json(cls, json_str: str) -> MessageContentDeltaSqlObject:
        """Create an instance of MessageContentDeltaSqlObject from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    def to_dict(
        self,
        hide_readonly_properties: bool = False,
    ) -> dict[str, Any]:
        """Returns the dictionary representation of the model using alias."""

        exclude_properties = set()

        if hide_readonly_properties:
            exclude_properties.update({})

        _dict = dict(
            self._iter(to_dict=True,
                       by_alias=True,
                       exclude=exclude_properties,
                       exclude_none=True))

        # override the default output from pydantic by calling `to_dict()` of confidence
        if self.confidence:
            _dict['confidence'] = self.confidence.to_dict()

        _dict[
            'type'] = MessageContentDelta.get_child_model_discriminator_value(
                'MessageContentDeltaSqlObject')

        return _dict

    def to_dict_without_readonly_properties(self) -> dict[str, Any]:
        """Return the dictionary representation of the model without readonly properties."""
        return self.to_dict(hide_readonly_properties=True)

    @classmethod
    def from_dict(cls, obj: dict) -> MessageContentDeltaSqlObject:
        """Create an instance of MessageContentDeltaSqlObject from a dict."""

        if obj is None:
            return None

        if type(obj) is not dict:
            return MessageContentDeltaSqlObject.parse_obj(obj)

        _obj = MessageContentDeltaSqlObject.parse_obj({
            "index":
            obj.get("index"),
            "statement_delta":
            obj.get("statement_delta"),
            "confidence":
            Confidence.from_dict(obj.get("confidence"))
            if obj.get("confidence") is not None else None,
        })

        return _obj


from typing import Optional, List, Dict

from snowflake.core.cortex_analyst._generated.models.confidence import Confidence

from snowflake.core.cortex_analyst._generated.models.message_content_delta import MessageContentDelta


class MessageContentDeltaSqlObjectModel(MessageContentDelta):

    def __init__(
        self,
        statement_delta: str,
        # optional properties
        index: Optional[int] = None,
        confidence: Optional[Confidence] = None,
    ):
        """A model object representing the MessageContentDeltaSqlObject resource.

        Constructs an object of type MessageContentDeltaSqlObject with the provided properties.

        Parameters
        __________
        statement_delta : str
            The delta of the sql statement, clients should concatenate all deltas for the same index

        index : int, optional
            The index of the content array this delta object represents

        confidence : Confidence, optional
        """

        super().__init__(index=index, )
        self.statement_delta = statement_delta
        self.confidence = confidence

    __properties = ["type", "index", "statement_delta", "confidence"]

    def __repr__(self) -> str:
        return repr(self._to_model())

    def _to_model(self):
        return MessageContentDeltaSqlObject(
            index=self.index,
            statement_delta=self.statement_delta,
            confidence=self.confidence._to_model()
            if self.confidence is not None else None,
        )

    @classmethod
    def _from_model(cls, model) -> MessageContentDeltaSqlObjectModel:
        return MessageContentDeltaSqlObjectModel(
            index=model.index,
            statement_delta=model.statement_delta,
            confidence=ConfidenceModel._from_model(model.confidence)
            if model.confidence is not None else None,
        )

    def to_dict(self):
        """Creates a dictionary of the properties from a MessageContentDeltaSqlObject.

        This method constructs a dictionary with the key-value entries corresponding to the properties of the MessageContentDeltaSqlObject object.

        Returns
        _______
        dict
            A dictionary object created using the input model.
        """
        return self._to_model().to_dict()

    @classmethod
    def from_dict(cls, obj: dict) -> MessageContentDeltaSqlObjectModel:
        """Creates an instance of MessageContentDeltaSqlObject from a dict.

        This method constructs a MessageContentDeltaSqlObject object from a dictionary with the key-value pairs of its properties.

        Parameters
        ----------
        obj : dict
            A dictionary whose keys and values correspond to the properties of the resource object.

        Returns
        _______
        MessageContentDeltaSqlObject
            A MessageContentDeltaSqlObject object created using the input dictionary; this will fail if the required properties are missing.
        """
        return cls._from_model(MessageContentDeltaSqlObject.from_dict(obj))


MessageContentDeltaSqlObject._model_class = MessageContentDeltaSqlObjectModel
