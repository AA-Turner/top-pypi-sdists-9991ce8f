"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class DiskSpec(google.protobuf.message.Message):
    """Disk specificaton."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Type:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _TypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[DiskSpec._Type.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        TYPE_UNSPECIFIED: DiskSpec._Type.ValueType  # 0
        """Disk type is not specified."""
        HDD: DiskSpec._Type.ValueType  # 1
        """HDD disk type."""
        SSD: DiskSpec._Type.ValueType  # 2
        """SSD disk type."""

    class Type(_Type, metaclass=_TypeEnumTypeWrapper): ...
    TYPE_UNSPECIFIED: DiskSpec.Type.ValueType  # 0
    """Disk type is not specified."""
    HDD: DiskSpec.Type.ValueType  # 1
    """HDD disk type."""
    SSD: DiskSpec.Type.ValueType  # 2
    """SSD disk type."""

    TYPE_FIELD_NUMBER: builtins.int
    SIZE_FIELD_NUMBER: builtins.int
    type: global___DiskSpec.Type.ValueType
    """Type of disk."""
    size: builtins.int
    """Size of disk."""
    def __init__(
        self,
        *,
        type: global___DiskSpec.Type.ValueType = ...,
        size: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["size", b"size", "type", b"type"]) -> None: ...

global___DiskSpec = DiskSpec
