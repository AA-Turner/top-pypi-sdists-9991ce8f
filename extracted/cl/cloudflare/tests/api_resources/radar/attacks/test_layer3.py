# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare._utils import parse_datetime
from cloudflare.types.radar.attacks import Layer3TimeseriesResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLayer3:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_timeseries(self, client: Cloudflare) -> None:
        layer3 = client.radar.attacks.layer3.timeseries()
        assert_matches_type(Layer3TimeseriesResponse, layer3, path=["response"])

    @parametrize
    def test_method_timeseries_with_all_params(self, client: Cloudflare) -> None:
        layer3 = client.radar.attacks.layer3.timeseries(
            agg_interval="1h",
            asn=["string"],
            continent=["string"],
            date_end=[parse_datetime("2019-12-27T18:11:19.117Z")],
            date_range=["7d"],
            date_start=[parse_datetime("2019-12-27T18:11:19.117Z")],
            direction="ORIGIN",
            format="JSON",
            ip_version=["IPv4"],
            location=["string"],
            metric="BYTES",
            name=["main_series"],
            normalization="MIN0_MAX",
            protocol=["UDP"],
        )
        assert_matches_type(Layer3TimeseriesResponse, layer3, path=["response"])

    @parametrize
    def test_raw_response_timeseries(self, client: Cloudflare) -> None:
        response = client.radar.attacks.layer3.with_raw_response.timeseries()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        layer3 = response.parse()
        assert_matches_type(Layer3TimeseriesResponse, layer3, path=["response"])

    @parametrize
    def test_streaming_response_timeseries(self, client: Cloudflare) -> None:
        with client.radar.attacks.layer3.with_streaming_response.timeseries() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            layer3 = response.parse()
            assert_matches_type(Layer3TimeseriesResponse, layer3, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncLayer3:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_timeseries(self, async_client: AsyncCloudflare) -> None:
        layer3 = await async_client.radar.attacks.layer3.timeseries()
        assert_matches_type(Layer3TimeseriesResponse, layer3, path=["response"])

    @parametrize
    async def test_method_timeseries_with_all_params(self, async_client: AsyncCloudflare) -> None:
        layer3 = await async_client.radar.attacks.layer3.timeseries(
            agg_interval="1h",
            asn=["string"],
            continent=["string"],
            date_end=[parse_datetime("2019-12-27T18:11:19.117Z")],
            date_range=["7d"],
            date_start=[parse_datetime("2019-12-27T18:11:19.117Z")],
            direction="ORIGIN",
            format="JSON",
            ip_version=["IPv4"],
            location=["string"],
            metric="BYTES",
            name=["main_series"],
            normalization="MIN0_MAX",
            protocol=["UDP"],
        )
        assert_matches_type(Layer3TimeseriesResponse, layer3, path=["response"])

    @parametrize
    async def test_raw_response_timeseries(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.radar.attacks.layer3.with_raw_response.timeseries()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        layer3 = await response.parse()
        assert_matches_type(Layer3TimeseriesResponse, layer3, path=["response"])

    @parametrize
    async def test_streaming_response_timeseries(self, async_client: AsyncCloudflare) -> None:
        async with async_client.radar.attacks.layer3.with_streaming_response.timeseries() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            layer3 = await response.parse()
            assert_matches_type(Layer3TimeseriesResponse, layer3, path=["response"])

        assert cast(Any, response.is_closed) is True
