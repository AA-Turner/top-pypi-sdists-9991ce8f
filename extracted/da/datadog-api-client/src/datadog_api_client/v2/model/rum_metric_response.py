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
    from datadog_api_client.v2.model.rum_metric_response_data import RumMetricResponseData


class RumMetricResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.rum_metric_response_data import RumMetricResponseData

        return {
            "data": (RumMetricResponseData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: Union[RumMetricResponseData, UnsetType] = unset, **kwargs):
        """
        The rum-based metric object.

        :param data: The rum-based metric properties.
        :type data: RumMetricResponseData, optional
        """
        if data is not unset:
            kwargs["data"] = data
        super().__init__(kwargs)
