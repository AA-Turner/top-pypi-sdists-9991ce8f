# coding: utf-8
"""
    Cortex Inference API.

    OpenAPI 3.0 specification for the Cortex REST API  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Contact: support@snowflake.com
    Generated by: https://openapi-generator.tech

    Do not edit this file manually.
"""

from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from typing import Union

from pydantic import BaseModel, ConfigDict, StrictStr, field_validator

from typing import Any, ClassVar, Dict, List, Optional


class StreamingTextContent(BaseModel):
    """A model object representing the StreamingTextContent resource.

    Constructs an object of type StreamingTextContent with the provided properties.

    Parameters
    __________
    type : str, optional
        Identifies this as text content.
    content : str, optional
        The actual text content of the message.
    """

    type: Optional[StrictStr] = None

    content: Optional[StrictStr] = None

    __properties = ["type", "content"]

    @field_validator('type')
    def type_validate_enum(cls, v):

        if v is None:
            return v
        if v not in ('text'):
            raise ValueError("must validate the enum values ('text')")
        return v

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
    def from_json(cls, json_str: str) -> StreamingTextContent:
        """Create an instance of StreamingTextContent from a JSON string."""
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

        return _dict

    def to_dict_without_readonly_properties(self) -> dict[str, Any]:
        """Return the dictionary representation of the model without readonly properties."""
        return self.to_dict(hide_readonly_properties=True)

    @classmethod
    def from_dict(cls, obj: dict) -> StreamingTextContent:
        """Create an instance of StreamingTextContent from a dict."""

        if obj is None:
            return None

        if type(obj) is not dict:
            return StreamingTextContent.parse_obj(obj)

        _obj = StreamingTextContent.parse_obj({
            "type": obj.get("type"),
            "content": obj.get("content"),
        })

        return _obj


from typing import Optional, List, Dict


class StreamingTextContentModel():

    def __init__(
        self,  # optional properties
        type: Optional[str] = None,
        content: Optional[str] = None,
    ):
        """A model object representing the StreamingTextContent resource.

        Constructs an object of type StreamingTextContent with the provided properties.

        Parameters
        __________
        type : str, optional
            Identifies this as text content.
        content : str, optional
            The actual text content of the message.
        """

        self.type = type
        self.content = content

    __properties = ["type", "content"]

    def __repr__(self) -> str:
        return repr(self._to_model())

    def _to_model(self):
        return StreamingTextContent(
            type=self.type,
            content=self.content,
        )

    @classmethod
    def _from_model(cls, model) -> StreamingTextContentModel:
        return StreamingTextContentModel(
            type=model.type,
            content=model.content,
        )

    def to_dict(self):
        """Creates a dictionary of the properties from a StreamingTextContent.

        This method constructs a dictionary with the key-value entries corresponding to the properties of the StreamingTextContent object.

        Returns
        _______
        dict
            A dictionary object created using the input model.
        """
        return self._to_model().to_dict()

    @classmethod
    def from_dict(cls, obj: dict) -> StreamingTextContentModel:
        """Creates an instance of StreamingTextContent from a dict.

        This method constructs a StreamingTextContent object from a dictionary with the key-value pairs of its properties.

        Parameters
        ----------
        obj : dict
            A dictionary whose keys and values correspond to the properties of the resource object.

        Returns
        _______
        StreamingTextContent
            A StreamingTextContent object created using the input dictionary; this will fail if the required properties are missing.
        """
        return cls._from_model(StreamingTextContent.from_dict(obj))


StreamingTextContent._model_class = StreamingTextContentModel
