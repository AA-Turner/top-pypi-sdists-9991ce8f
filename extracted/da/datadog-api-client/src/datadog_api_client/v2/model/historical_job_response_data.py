# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.historical_job_response_attributes import HistoricalJobResponseAttributes
    from datadog_api_client.v2.model.historical_job_data_type import HistoricalJobDataType


class HistoricalJobResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.historical_job_response_attributes import HistoricalJobResponseAttributes
        from datadog_api_client.v2.model.historical_job_data_type import HistoricalJobDataType

        return {
            "attributes": (HistoricalJobResponseAttributes,),
            "id": (str,),
            "type": (HistoricalJobDataType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[HistoricalJobResponseAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        type: Union[HistoricalJobDataType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Historical job response data.

        :param attributes: Historical job attributes.
        :type attributes: HistoricalJobResponseAttributes, optional

        :param id: ID of the job.
        :type id: str, optional

        :param type: Type of payload.
        :type type: HistoricalJobDataType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
