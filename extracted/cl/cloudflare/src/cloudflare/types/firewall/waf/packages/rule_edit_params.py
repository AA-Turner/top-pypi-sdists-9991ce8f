# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["RuleEditParams"]


class RuleEditParams(TypedDict, total=False):
    zone_id: Required[str]
    """Defines an identifier of a schema."""

    package_id: Required[str]
    """Defines the unique identifier of a WAF package."""

    mode: Literal["default", "disable", "simulate", "block", "challenge", "on", "off"]
    """Defines the mode/action of the rule when triggered.

    You must use a value from the `allowed_modes` array of the current rule.
    """
