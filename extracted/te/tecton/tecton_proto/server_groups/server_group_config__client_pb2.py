# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/server_groups/server_group_config__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.realtime import instance_group__client_pb2 as tecton__proto_dot_realtime_dot_instance__group____client__pb2
from tecton_proto.server_groups import server_group_states__client_pb2 as tecton__proto_dot_server__groups_dot_server__group__states____client__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n<tecton_proto/server_groups/server_group_config__client.proto\x12\x1atecton_proto.server_groups\x1a\x32tecton_proto/realtime/instance_group__client.proto\x1a<tecton_proto/server_groups/server_group_states__client.proto\"\x86\x01\n\x18ServerGroupClusterConfig\x12j\n\x16transform_server_group\x18\x01 \x03(\x0b\x32\x34.tecton_proto.server_groups.TransformServerGroupInfoR\x14transformServerGroup\"\xfa\x03\n\x18TransformServerGroupInfo\x12&\n\x0fserver_group_id\x18\x01 \x01(\tR\rserverGroupId\x12\\\n\x12\x61utoscaling_policy\x18\x02 \x01(\x0b\x32-.tecton_proto.server_groups.AutoscalingPolicyR\x11\x61utoscalingPolicy\x12p\n\x19\x61ws_instance_group_config\x18\x03 \x01(\x0b\x32\x33.tecton_proto.realtime.AWSInstanceGroupUpdateConfigH\x00R\x16\x61wsInstanceGroupConfig\x12\x83\x01\n\x15\x65nvironment_variables\x18\x04 \x03(\x0b\x32N.tecton_proto.server_groups.TransformServerGroupInfo.EnvironmentVariablesEntryR\x14\x65nvironmentVariables\x1aG\n\x19\x45nvironmentVariablesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\x17\n\x15instance_group_configB\x1b\n\x17\x63om.tecton.servergroupsP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.server_groups.server_group_config__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027com.tecton.servergroupsP\001'
  _TRANSFORMSERVERGROUPINFO_ENVIRONMENTVARIABLESENTRY._options = None
  _TRANSFORMSERVERGROUPINFO_ENVIRONMENTVARIABLESENTRY._serialized_options = b'8\001'
  _SERVERGROUPCLUSTERCONFIG._serialized_start=207
  _SERVERGROUPCLUSTERCONFIG._serialized_end=341
  _TRANSFORMSERVERGROUPINFO._serialized_start=344
  _TRANSFORMSERVERGROUPINFO._serialized_end=850
  _TRANSFORMSERVERGROUPINFO_ENVIRONMENTVARIABLESENTRY._serialized_start=754
  _TRANSFORMSERVERGROUPINFO_ENVIRONMENTVARIABLESENTRY._serialized_end=825
# @@protoc_insertion_point(module_scope)
