# coding: utf-8
"""
    Snowflake API Integration API.

    The Snowflake API Integration API is a REST API that you can use to access, update, and perform certain actions on API Integration resource in a Snowflake database.  # noqa: E501

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

from snowflake.core.api_integration._generated.models.api_hook import ApiHook

from pydantic import ConfigDict, StrictStr, field_validator

from typing import Any, ClassVar, Dict, List, Optional


class GoogleCloudHook(ApiHook):
    """A model object representing the GoogleCloudHook resource.

    Constructs an object of type GoogleCloudHook with the provided properties.

    Parameters
    __________
    api_provider : str

    google_audience : str
        Used as an audience claim when generating the JTW (JSON Web Token) to authenticate to the Google API Gateway.
    api_key : str, optional
        An alphanumeric string that is used to identify API clients and control access to the API, also called a subscription key.
    """

    api_provider: StrictStr

    google_audience: StrictStr

    api_key: Optional[StrictStr] = None

    __properties = ["type"]

    @field_validator('api_provider')
    def api_provider_validate_enum(cls, v):

        if v not in ('GOOGLE_API_GATEWAY'):
            raise ValueError(
                "must validate the enum values ('GOOGLE_API_GATEWAY')")
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
    def from_json(cls, json_str: str) -> GoogleCloudHook:
        """Create an instance of GoogleCloudHook from a JSON string."""
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

        # set to None if api_key (nullable) is None
        if self.api_key is None:
            _dict['api_key'] = None

        _dict['type'] = ApiHook.get_child_model_discriminator_value(
            'GoogleCloudHook')

        return _dict

    def to_dict_without_readonly_properties(self) -> dict[str, Any]:
        """Return the dictionary representation of the model without readonly properties."""
        return self.to_dict(hide_readonly_properties=True)

    @classmethod
    def from_dict(cls, obj: dict) -> GoogleCloudHook:
        """Create an instance of GoogleCloudHook from a dict."""

        if obj is None:
            return None

        if type(obj) is not dict:
            return GoogleCloudHook.parse_obj(obj)

        _obj = GoogleCloudHook.parse_obj({
            "api_provider":
            obj.get("api_provider"),
            "google_audience":
            obj.get("google_audience"),
            "api_key":
            obj.get("api_key"),
        })

        return _obj


from typing import Optional, List, Dict

from snowflake.core.api_integration._generated.models.api_hook import ApiHook


class GoogleCloudHookModel(ApiHook):

    def __init__(
        self,
        api_provider: str,
        google_audience: str,
        # optional properties
        api_key: Optional[str] = None,
    ):
        """A model object representing the GoogleCloudHook resource.

        Constructs an object of type GoogleCloudHook with the provided properties.

        Parameters
        __________
        api_provider : str

        google_audience : str
            Used as an audience claim when generating the JTW (JSON Web Token) to authenticate to the Google API Gateway.
        api_key : str, optional
            An alphanumeric string that is used to identify API clients and control access to the API, also called a subscription key.
        """

        super().__init__()
        self.api_provider = api_provider
        self.google_audience = google_audience
        self.api_key = api_key

    __properties = ["type"]

    def __repr__(self) -> str:
        return repr(self._to_model())

    def _to_model(self):
        return GoogleCloudHook(
            api_provider=self.api_provider,
            google_audience=self.google_audience,
            api_key=self.api_key,
        )

    @classmethod
    def _from_model(cls, model) -> GoogleCloudHookModel:
        return GoogleCloudHookModel(
            api_provider=model.api_provider,
            google_audience=model.google_audience,
            api_key=model.api_key,
        )

    def to_dict(self):
        """Creates a dictionary of the properties from a GoogleCloudHook.

        This method constructs a dictionary with the key-value entries corresponding to the properties of the GoogleCloudHook object.

        Returns
        _______
        dict
            A dictionary object created using the input model.
        """
        return self._to_model().to_dict()

    @classmethod
    def from_dict(cls, obj: dict) -> GoogleCloudHookModel:
        """Creates an instance of GoogleCloudHook from a dict.

        This method constructs a GoogleCloudHook object from a dictionary with the key-value pairs of its properties.

        Parameters
        ----------
        obj : dict
            A dictionary whose keys and values correspond to the properties of the resource object.

        Returns
        _______
        GoogleCloudHook
            A GoogleCloudHook object created using the input dictionary; this will fail if the required properties are missing.
        """
        return cls._from_model(GoogleCloudHook.from_dict(obj))


GoogleCloudHook._model_class = GoogleCloudHookModel
