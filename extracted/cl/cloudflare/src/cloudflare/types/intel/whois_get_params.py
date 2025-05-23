# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["WhoisGetParams"]


class WhoisGetParams(TypedDict, total=False):
    account_id: Required[str]
    """Use to uniquely identify or reference the resource."""

    domain: str
