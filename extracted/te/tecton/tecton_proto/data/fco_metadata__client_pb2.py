# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/fco_metadata__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from tecton_proto.common import framework_version__client_pb2 as tecton__proto_dot_common_dot_framework__version____client__pb2
from tecton_proto.common import id__client_pb2 as tecton__proto_dot_common_dot_id____client__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,tecton_proto/data/fco_metadata__client.proto\x12\x11tecton_proto.data\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x33tecton_proto/common/framework_version__client.proto\x1a$tecton_proto/common/id__client.proto\"\xd5\x05\n\x0b\x46\x63oMetadata\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x02 \x01(\tR\x0b\x64\x65scription\x12\x39\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x14\n\x05owner\x18\x04 \x01(\tR\x05owner\x12(\n\x10last_modified_by\x18\r \x01(\tR\x0elastModifiedBy\x12\x1f\n\x0bis_archived\x18\x05 \x01(\x08R\nisArchived\x12\x1c\n\tworkspace\x18\x07 \x01(\tR\tworkspace\x12\x45\n\x12workspace_state_id\x18\x0e \x01(\x0b\x32\x17.tecton_proto.common.IdR\x10workspaceStateId\x12\x16\n\x06\x66\x61mily\x18\x08 \x01(\tR\x06\x66\x61mily\x12\x14\n\x05scope\x18\t \x01(\tR\x05scope\x12#\n\rsource_lineno\x18\n \x01(\tR\x0csourceLineno\x12\'\n\x0fsource_filename\x18\x0b \x01(\tR\x0esourceFilename\x12<\n\x04tags\x18\x0c \x03(\x0b\x32(.tecton_proto.data.FcoMetadata.TagsEntryR\x04tags\x12R\n\x11\x66ramework_version\x18\x0f \x01(\x0e\x32%.tecton_proto.common.FrameworkVersionR\x10\x66rameworkVersion\x12\x42\n\x0flast_updated_at\x18\x10 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\rlastUpdatedAt\x1a\x37\n\tTagsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01J\x04\x08\x06\x10\x07\x42;\n\x0f\x63om.tecton.dataP\x01Z&github.com/tecton-ai/tecton_proto/data')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.fco_metadata__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001Z&github.com/tecton-ai/tecton_proto/data'
  _FCOMETADATA_TAGSENTRY._options = None
  _FCOMETADATA_TAGSENTRY._serialized_options = b'8\001'
  _FCOMETADATA._serialized_start=192
  _FCOMETADATA._serialized_end=917
  _FCOMETADATA_TAGSENTRY._serialized_start=856
  _FCOMETADATA_TAGSENTRY._serialized_end=911
# @@protoc_insertion_point(module_scope)
