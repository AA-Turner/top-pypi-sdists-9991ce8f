# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/fco__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.common import id__client_pb2 as tecton__proto_dot_common_dot_id____client__pb2
from tecton_proto.data import entity__client_pb2 as tecton__proto_dot_data_dot_entity____client__pb2
from tecton_proto.data import feature_service__client_pb2 as tecton__proto_dot_data_dot_feature__service____client__pb2
from tecton_proto.data import feature_view__client_pb2 as tecton__proto_dot_data_dot_feature__view____client__pb2
from tecton_proto.data import resource_provider__client_pb2 as tecton__proto_dot_data_dot_resource__provider____client__pb2
from tecton_proto.data import server_group__client_pb2 as tecton__proto_dot_data_dot_server__group____client__pb2
from tecton_proto.data import transformation__client_pb2 as tecton__proto_dot_data_dot_transformation____client__pb2
from tecton_proto.data import virtual_data_source__client_pb2 as tecton__proto_dot_data_dot_virtual__data__source____client__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#tecton_proto/data/fco__client.proto\x12\x11tecton_proto.data\x1a$tecton_proto/common/id__client.proto\x1a&tecton_proto/data/entity__client.proto\x1a/tecton_proto/data/feature_service__client.proto\x1a,tecton_proto/data/feature_view__client.proto\x1a\x31tecton_proto/data/resource_provider__client.proto\x1a,tecton_proto/data/server_group__client.proto\x1a.tecton_proto/data/transformation__client.proto\x1a\x33tecton_proto/data/virtual_data_source__client.proto\"\x9e\x04\n\x03\x46\x63o\x12V\n\x13virtual_data_source\x18\x01 \x01(\x0b\x32$.tecton_proto.data.VirtualDataSourceH\x00R\x11virtualDataSource\x12\x33\n\x06\x65ntity\x18\x02 \x01(\x0b\x32\x19.tecton_proto.data.EntityH\x00R\x06\x65ntity\x12\x43\n\x0c\x66\x65\x61ture_view\x18\x06 \x01(\x0b\x32\x1e.tecton_proto.data.FeatureViewH\x00R\x0b\x66\x65\x61tureView\x12L\n\x0f\x66\x65\x61ture_service\x18\x04 \x01(\x0b\x32!.tecton_proto.data.FeatureServiceH\x00R\x0e\x66\x65\x61tureService\x12K\n\x0etransformation\x18\x07 \x01(\x0b\x32!.tecton_proto.data.TransformationH\x00R\x0etransformation\x12\x43\n\x0cserver_group\x18\x08 \x01(\x0b\x32\x1e.tecton_proto.data.ServerGroupH\x00R\x0bserverGroup\x12R\n\x11resource_provider\x18\t \x01(\x0b\x32#.tecton_proto.data.ResourceProviderH\x00R\x10resourceProviderB\x05\n\x03\x66\x63oJ\x04\x08\x03\x10\x04J\x04\x08\x05\x10\x06\"\xd3\x01\n\x0c\x46\x63oContainer\x12\x32\n\x08root_ids\x18\x01 \x03(\x0b\x32\x17.tecton_proto.common.IdR\x07rootIds\x12*\n\x04\x66\x63os\x18\x02 \x03(\x0b\x32\x16.tecton_proto.data.FcoR\x04\x66\x63os\x12\x1c\n\tworkspace\x18\x03 \x01(\tR\tworkspace\x12\x45\n\x12workspace_state_id\x18\x04 \x01(\x0b\x32\x17.tecton_proto.common.IdR\x10workspaceStateIdB;\n\x0f\x63om.tecton.dataP\x01Z&github.com/tecton-ai/tecton_proto/data')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.fco__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001Z&github.com/tecton-ai/tecton_proto/data'
  _FCO._serialized_start=430
  _FCO._serialized_end=972
  _FCOCONTAINER._serialized_start=975
  _FCOCONTAINER._serialized_end=1186
# @@protoc_insertion_point(module_scope)
