# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: yandex/cloud/mdb/greenplum/v1/host.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'yandex/cloud/mdb/greenplum/v1/host.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud.mdb.greenplum.v1 import config_pb2 as yandex_dot_cloud_dot_mdb_dot_greenplum_dot_v1_dot_config__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(yandex/cloud/mdb/greenplum/v1/host.proto\x12\x1dyandex.cloud.mdb.greenplum.v1\x1a*yandex/cloud/mdb/greenplum/v1/config.proto\x1a\x1dyandex/cloud/validation.proto\"\xb3\x03\n\x04Host\x12\x1a\n\x04name\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=63\x12\x12\n\ncluster_id\x18\x02 \x01(\t\x12\x0f\n\x07zone_id\x18\x03 \x01(\t\x12\x36\n\x04type\x18\x04 \x01(\x0e\x32(.yandex.cloud.mdb.greenplum.v1.Host.Type\x12;\n\tresources\x18\x05 \x01(\x0b\x32(.yandex.cloud.mdb.greenplum.v1.Resources\x12:\n\x06health\x18\x06 \x01(\x0e\x32*.yandex.cloud.mdb.greenplum.v1.Host.Health\x12\x11\n\tsubnet_id\x18\x07 \x01(\t\x12\x18\n\x10\x61ssign_public_ip\x18\x08 \x01(\x08\"B\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\n\n\x06MASTER\x10\x01\x12\x0b\n\x07REPLICA\x10\x02\x12\x0b\n\x07SEGMENT\x10\x03\"H\n\x06Health\x12\x0b\n\x07UNKNOWN\x10\x00\x12\t\n\x05\x41LIVE\x10\x01\x12\x08\n\x04\x44\x45\x41\x44\x10\x02\x12\x0c\n\x08\x44\x45GRADED\x10\x03\x12\x0e\n\nUNBALANCED\x10\x04\x42p\n!yandex.cloud.api.mdb.greenplum.v1ZKgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/greenplum/v1;greenplumb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.mdb.greenplum.v1.host_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n!yandex.cloud.api.mdb.greenplum.v1ZKgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/greenplum/v1;greenplum'
  _globals['_HOST'].fields_by_name['name']._loaded_options = None
  _globals['_HOST'].fields_by_name['name']._serialized_options = b'\350\3071\001\212\3101\004<=63'
  _globals['_HOST']._serialized_start=151
  _globals['_HOST']._serialized_end=586
  _globals['_HOST_TYPE']._serialized_start=446
  _globals['_HOST_TYPE']._serialized_end=512
  _globals['_HOST_HEALTH']._serialized_start=514
  _globals['_HOST_HEALTH']._serialized_end=586
# @@protoc_insertion_point(module_scope)
