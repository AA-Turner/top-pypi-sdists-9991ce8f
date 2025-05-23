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

from pydantic import BaseModel, ConfigDict, StrictStr

from typing import Any, ClassVar, Dict, List, Optional


class ToolToolSpecInputSchema(BaseModel):
    """A model object representing the ToolToolSpecInputSchema resource.

    Constructs an object of type ToolToolSpecInputSchema with the provided properties.

    Parameters
    __________
    type : str, optional
        The type of the input schema object
    properties : object, optional
        Definitions of each input parameter
    required : List[str], optional
        List of required input parameter names
    """

    type: Optional[StrictStr] = None

    properties: Optional[Dict[str, Any]] = None

    required: Optional[List[StrictStr]] = None

    additional_properties: dict[str, Any] = {}

    __properties = ["type", "properties", "required"]

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
    def from_json(cls, json_str: str) -> ToolToolSpecInputSchema:
        """Create an instance of ToolToolSpecInputSchema from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    def to_dict(
        self,
        hide_readonly_properties: bool = False,
    ) -> dict[str, Any]:
        """Returns the dictionary representation of the model using alias."""

        exclude_properties = {"additional_properties"}

        if hide_readonly_properties:
            exclude_properties.update({})

        _dict = dict(
            self._iter(to_dict=True,
                       by_alias=True,
                       exclude=exclude_properties,
                       exclude_none=True))

        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    def to_dict_without_readonly_properties(self) -> dict[str, Any]:
        """Return the dictionary representation of the model without readonly properties."""
        return self.to_dict(hide_readonly_properties=True)

    @classmethod
    def from_dict(cls, obj: dict) -> ToolToolSpecInputSchema:
        """Create an instance of ToolToolSpecInputSchema from a dict."""

        if obj is None:
            return None

        if type(obj) is not dict:
            return ToolToolSpecInputSchema.parse_obj(obj)

        _obj = ToolToolSpecInputSchema.parse_obj({
            "type":
            obj.get("type"),
            "properties":
            obj.get("properties"),
            "required":
            obj.get("required"),
        })

        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


from typing import Optional, List, Dict


class ToolToolSpecInputSchemaModel():

    def __init__(
        self,  # optional properties
        type: Optional[str] = None,
        properties: Optional[object] = None,
        required: Optional[List[str]] = None,
    ):
        """A model object representing the ToolToolSpecInputSchema resource.

        Constructs an object of type ToolToolSpecInputSchema with the provided properties.

        Parameters
        __________
        type : str, optional
            The type of the input schema object
        properties : object, optional
            Definitions of each input parameter
        required : List[str], optional
            List of required input parameter names
        """

        self.type = type
        self.properties = properties
        self.required = required

    additional_properties: dict[str, Any] = {}

    __properties = ["type", "properties", "required"]

    def __repr__(self) -> str:
        return repr(self._to_model())

    def _to_model(self):
        return ToolToolSpecInputSchema(
            type=self.type,
            properties=self.properties,
            required=self.required,
        )

    @classmethod
    def _from_model(cls, model) -> ToolToolSpecInputSchemaModel:
        return ToolToolSpecInputSchemaModel(
            type=model.type,
            properties=model.properties,
            required=model.required,
        )

    def to_dict(self):
        """Creates a dictionary of the properties from a ToolToolSpecInputSchema.

        This method constructs a dictionary with the key-value entries corresponding to the properties of the ToolToolSpecInputSchema object.

        Returns
        _______
        dict
            A dictionary object created using the input model.
        """
        return self._to_model().to_dict()

    @classmethod
    def from_dict(cls, obj: dict) -> ToolToolSpecInputSchemaModel:
        """Creates an instance of ToolToolSpecInputSchema from a dict.

        This method constructs a ToolToolSpecInputSchema object from a dictionary with the key-value pairs of its properties.

        Parameters
        ----------
        obj : dict
            A dictionary whose keys and values correspond to the properties of the resource object.

        Returns
        _______
        ToolToolSpecInputSchema
            A ToolToolSpecInputSchema object created using the input dictionary; this will fail if the required properties are missing.
        """
        return cls._from_model(ToolToolSpecInputSchema.from_dict(obj))


ToolToolSpecInputSchema._model_class = ToolToolSpecInputSchemaModel
