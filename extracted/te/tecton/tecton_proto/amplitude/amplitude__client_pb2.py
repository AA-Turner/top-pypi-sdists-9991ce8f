# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/amplitude/amplitude__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from tecton_proto.amplitude import client_logging__client_pb2 as tecton__proto_dot_amplitude_dot_client__logging____client__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.tecton_proto/amplitude/amplitude__client.proto\x12\x16tecton_proto.amplitude\x1a\x1egoogle/protobuf/duration.proto\x1a\x33tecton_proto/amplitude/client_logging__client.proto\"\xd3\x02\n\x0e\x41mplitudeEvent\x12\x17\n\x07user_id\x18\x01 \x01(\tR\x06userId\x12\x1b\n\tdevice_id\x18\x08 \x01(\tR\x08\x64\x65viceId\x12\x1d\n\nevent_type\x18\x02 \x01(\tR\teventType\x12\x1a\n\x08platform\x18\x03 \x01(\tR\x08platform\x12\x1d\n\nsession_id\x18\x05 \x01(\x03R\tsessionId\x12\x1c\n\ttimestamp\x18\x06 \x01(\x03R\ttimestamp\x12\x17\n\x07os_name\x18\t \x01(\tR\x06osName\x12\x1d\n\nos_version\x18\n \x01(\tR\tosVersion\x12[\n\x10\x65vent_properties\x18\x07 \x01(\x0b\x32\x30.tecton_proto.amplitude.AmplitudeEventPropertiesR\x0f\x65ventProperties\"\xfc\x06\n\x18\x41mplitudeEventProperties\x12!\n\x0c\x63luster_name\x18\x01 \x01(\tR\x0b\x63lusterName\x12\x1c\n\tworkspace\x18\x02 \x01(\tR\tworkspace\x12\x1f\n\x0bsdk_version\x18\x04 \x01(\tR\nsdkVersion\x12%\n\x0epython_version\x18\x0b \x01(\tR\rpythonVersion\x12@\n\x0e\x65xecution_time\x18\x05 \x01(\x0b\x32\x19.google.protobuf.DurationR\rexecutionTime\x12$\n\x0enum_total_fcos\x18\x06 \x01(\x03R\x0cnumTotalFcos\x12(\n\x10num_fcos_changed\x18\x07 \x01(\x03R\x0enumFcosChanged\x12\x1e\n\x0bnum_v3_fcos\x18\x0c \x01(\x03R\tnumV3Fcos\x12\x1e\n\x0bnum_v5_fcos\x18\r \x01(\x03R\tnumV5Fcos\x12-\n\x12suppress_recreates\x18\x0e \x01(\x08R\x11suppressRecreates\x12\x19\n\x08json_out\x18\x10 \x01(\x08R\x07jsonOut\x12\x18\n\x07success\x18\x08 \x01(\x08R\x07success\x12#\n\rerror_message\x18\t \x01(\tR\x0c\x65rrorMessage\x12!\n\x0cnum_warnings\x18\x0f \x01(\x03R\x0bnumWarnings\x12T\n\x06params\x18\x11 \x03(\x0b\x32<.tecton_proto.amplitude.AmplitudeEventProperties.ParamsEntryR\x06params\x12_\n\x15sdk_method_invocation\x18\x03 \x01(\x0b\x32+.tecton_proto.amplitude.SDKMethodInvocationR\x13sdkMethodInvocation\x12\x16\n\x06status\x18\n \x01(\tR\x06status\x12O\n\x0f\x63\x61ller_identity\x18\x12 \x01(\x0b\x32&.tecton_proto.amplitude.CallerIdentityR\x0e\x63\x61llerIdentity\x1a\x39\n\x0bParamsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"Y\n\x0e\x43\x61llerIdentity\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12#\n\ridentity_type\x18\x03 \x01(\tR\x0cidentityType\"h\n\rUploadRequest\x12\x17\n\x07\x61pi_key\x18\x01 \x01(\tR\x06\x61piKey\x12>\n\x06\x65vents\x18\x02 \x03(\x0b\x32&.tecton_proto.amplitude.AmplitudeEventR\x06\x65vents\"\xe4\x01\n\x0eUploadResponse\x12\x12\n\x04\x63ode\x18\x01 \x01(\x05R\x04\x63ode\x12\'\n\x0f\x65vents_ingested\x18\x02 \x01(\x05R\x0e\x65ventsIngested\x12,\n\x12payload_size_bytes\x18\x03 \x01(\x05R\x10payloadSizeBytes\x12,\n\x12server_upload_time\x18\x04 \x01(\x03R\x10serverUploadTime\x12\x14\n\x05\x65rror\x18\x05 \x01(\tR\x05\x65rror\x12#\n\rmissing_field\x18\x06 \x01(\tR\x0cmissingFieldBE\n\x14\x63om.tecton.amplitudeP\x01Z+github.com/tecton-ai/tecton_proto/amplitude')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.amplitude.amplitude__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024com.tecton.amplitudeP\001Z+github.com/tecton-ai/tecton_proto/amplitude'
  _AMPLITUDEEVENTPROPERTIES_PARAMSENTRY._options = None
  _AMPLITUDEEVENTPROPERTIES_PARAMSENTRY._serialized_options = b'8\001'
  _AMPLITUDEEVENT._serialized_start=160
  _AMPLITUDEEVENT._serialized_end=499
  _AMPLITUDEEVENTPROPERTIES._serialized_start=502
  _AMPLITUDEEVENTPROPERTIES._serialized_end=1394
  _AMPLITUDEEVENTPROPERTIES_PARAMSENTRY._serialized_start=1337
  _AMPLITUDEEVENTPROPERTIES_PARAMSENTRY._serialized_end=1394
  _CALLERIDENTITY._serialized_start=1396
  _CALLERIDENTITY._serialized_end=1485
  _UPLOADREQUEST._serialized_start=1487
  _UPLOADREQUEST._serialized_end=1591
  _UPLOADRESPONSE._serialized_start=1594
  _UPLOADRESPONSE._serialized_end=1822
# @@protoc_insertion_point(module_scope)
