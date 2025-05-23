# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: yandex/cloud/ai/dataset/v1/dataset.proto
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
    'yandex/cloud/ai/dataset/v1/dataset.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(yandex/cloud/ai/dataset/v1/dataset.proto\x12\x1ayandex.cloud.ai.dataset.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xbd\x05\n\x0b\x44\x61tasetInfo\x12\x12\n\ndataset_id\x18\x01 \x01(\t\x12\x11\n\tfolder_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x10\n\x08metadata\x18\x05 \x01(\t\x12>\n\x06status\x18\x06 \x01(\x0e\x32..yandex.cloud.ai.dataset.v1.DatasetInfo.Status\x12\x11\n\ttask_type\x18\x07 \x01(\t\x12.\n\ncreated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04rows\x18\n \x01(\x03\x12\x12\n\nsize_bytes\x18\x0b \x01(\x03\x12\x19\n\rcreated_by_id\x18\x0c \x01(\tB\x02\x18\x01\x12\x43\n\x06labels\x18\r \x03(\x0b\x32\x33.yandex.cloud.ai.dataset.v1.DatasetInfo.LabelsEntry\x12\x12\n\ncreated_by\x18\x0e \x01(\t\x12\x12\n\nupdated_by\x18\x0f \x01(\t\x12\x45\n\x10validation_error\x18\x15 \x03(\x0b\x32+.yandex.cloud.ai.dataset.v1.ValidationError\x12\x16\n\x0e\x61llow_data_log\x18\x16 \x01(\x08\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"a\n\x06Status\x12\x16\n\x12STATUS_UNSPECIFIED\x10\x00\x12\t\n\x05\x44RAFT\x10\x01\x12\x0e\n\nVALIDATING\x10\x02\x12\t\n\x05READY\x10\x03\x12\x0b\n\x07INVALID\x10\x04\x12\x0c\n\x08\x44\x45LETING\x10\x05J\x04\x08\x10\x10\x15\"P\n\x0fValidationError\x12\r\n\x05\x65rror\x18\x01 \x01(\t\x12\x19\n\x11\x65rror_description\x18\x02 \x01(\t\x12\x13\n\x0brow_numbers\x18\x03 \x03(\x03\"O\n\x13\x44\x61tasetUploadSchema\x12\x11\n\ttask_type\x18\x01 \x01(\t\x12\x15\n\rupload_format\x18\x02 \x01(\t\x12\x0e\n\x06schema\x18\x03 \x01(\t\"2\n\x16\x44\x61tasetFileDownloadUrl\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\tBe\n\x1eyandex.cloud.api.ai.dataset.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/ai/dataset/v1;fomob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.ai.dataset.v1.dataset_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\036yandex.cloud.api.ai.dataset.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/ai/dataset/v1;fomo'
  _globals['_DATASETINFO_LABELSENTRY']._loaded_options = None
  _globals['_DATASETINFO_LABELSENTRY']._serialized_options = b'8\001'
  _globals['_DATASETINFO'].fields_by_name['created_by_id']._loaded_options = None
  _globals['_DATASETINFO'].fields_by_name['created_by_id']._serialized_options = b'\030\001'
  _globals['_DATASETINFO']._serialized_start=106
  _globals['_DATASETINFO']._serialized_end=807
  _globals['_DATASETINFO_LABELSENTRY']._serialized_start=657
  _globals['_DATASETINFO_LABELSENTRY']._serialized_end=702
  _globals['_DATASETINFO_STATUS']._serialized_start=704
  _globals['_DATASETINFO_STATUS']._serialized_end=801
  _globals['_VALIDATIONERROR']._serialized_start=809
  _globals['_VALIDATIONERROR']._serialized_end=889
  _globals['_DATASETUPLOADSCHEMA']._serialized_start=891
  _globals['_DATASETUPLOADSCHEMA']._serialized_end=970
  _globals['_DATASETFILEDOWNLOADURL']._serialized_start=972
  _globals['_DATASETFILEDOWNLOADURL']._serialized_end=1022
# @@protoc_insertion_point(module_scope)
