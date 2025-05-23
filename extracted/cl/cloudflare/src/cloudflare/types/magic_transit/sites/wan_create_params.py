# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .wan_static_addressing_param import WANStaticAddressingParam

__all__ = ["WANCreateParams"]


class WANCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier"""

    physport: Required[int]

    name: str

    priority: int

    static_addressing: WANStaticAddressingParam
    """(optional) if omitted, use DHCP.

    Submit secondary_address when site is in high availability mode.
    """

    vlan_tag: int
    """VLAN ID. Use zero for untagged."""
