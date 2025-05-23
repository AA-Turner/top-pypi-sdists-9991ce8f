# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/dataobs/validation_task__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from tecton_proto.common import fco_locator__client_pb2 as tecton__proto_dot_common_dot_fco__locator____client__pb2
from tecton_proto.common import id__client_pb2 as tecton__proto_dot_common_dot_id____client__pb2
from tecton_proto.dataobs import expectation__client_pb2 as tecton__proto_dot_dataobs_dot_expectation____client__pb2
from tecton_proto.dataobs import validation__client_pb2 as tecton__proto_dot_dataobs_dot_validation____client__pb2
from tecton_proto.dataobs import validation_task_params__client_pb2 as tecton__proto_dot_dataobs_dot_validation__task__params____client__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2tecton_proto/dataobs/validation_task__client.proto\x12\x14tecton_proto.dataobs\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a-tecton_proto/common/fco_locator__client.proto\x1a$tecton_proto/common/id__client.proto\x1a.tecton_proto/dataobs/expectation__client.proto\x1a-tecton_proto/dataobs/validation__client.proto\x1a\x39tecton_proto/dataobs/validation_task_params__client.proto\"\xc7\x05\n\x0eValidationTask\x12\x43\n\x11validation_job_id\x18\x01 \x01(\x0b\x32\x17.tecton_proto.common.IdR\x0fvalidationJobId\x12S\n\x14\x66\x65\x61ture_view_locator\x18\x02 \x01(\x0b\x32!.tecton_proto.common.IdFcoLocatorR\x12\x66\x65\x61tureViewLocator\x12X\n\x13metric_expectations\x18\x03 \x03(\x0b\x32\'.tecton_proto.dataobs.MetricExpectationR\x12metricExpectations\x12H\n\x12\x66\x65\x61ture_start_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x10\x66\x65\x61tureStartTime\x12\x44\n\x10\x66\x65\x61ture_end_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0e\x66\x65\x61tureEndTime\x12\x45\n\ttask_type\x18\x08 \x01(\x0e\x32(.tecton_proto.dataobs.ValidationTaskTypeR\x08taskType\x12\x37\n\x07timeout\x18\t \x01(\x0b\x32\x19.google.protobuf.DurationB\x02\x18\x01R\x07timeout\x12V\n\x12\x64ynamo_data_source\x18\x06 \x01(\x0b\x32&.tecton_proto.dataobs.DynamoDataSourceH\x00R\x10\x64ynamoDataSource\x12J\n\x0es3_data_source\x18\x07 \x01(\x0b\x32\".tecton_proto.dataobs.S3DataSourceH\x00R\x0cs3DataSourceB\r\n\x0b\x64\x61ta_source\"\x9f\x04\n\x14ValidationTaskResult\x12\x1c\n\tworkspace\x18\x01 \x01(\tR\tworkspace\x12\x45\n\x12\x66\x65\x61ture_package_id\x18\x02 \x01(\x0b\x32\x17.tecton_proto.common.IdR\x10\x66\x65\x61turePackageId\x12\x43\n\x11validation_job_id\x18\x03 \x01(\x0b\x32\x17.tecton_proto.common.IdR\x0fvalidationJobId\x12H\n\x12\x66\x65\x61ture_start_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x10\x66\x65\x61tureStartTime\x12\x44\n\x10\x66\x65\x61ture_end_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0e\x66\x65\x61tureEndTime\x12\x41\n\x07results\x18\x06 \x03(\x0b\x32\'.tecton_proto.dataobs.ExpectationResultR\x07results\x12\x45\n\x07metrics\x18\x07 \x01(\x0b\x32+.tecton_proto.dataobs.ValidationTaskMetricsR\x07metrics\x12\x43\n\x0fvalidation_time\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0evalidationTime\"\xbc\x01\n\x15ValidationTaskMetrics\x12(\n\x10metric_rows_read\x18\x01 \x01(\rR\x0emetricRowsRead\x12*\n\x11\x66\x65\x61ture_rows_read\x18\x02 \x01(\rR\x0f\x66\x65\x61tureRowsRead\x12M\n\x15query_execution_times\x18\x03 \x03(\x0b\x32\x19.google.protobuf.DurationR\x13queryExecutionTimes*^\n\x12ValidationTaskType\x12 \n\x1cVALIDATION_TASK_TYPE_UNKNOWN\x10\x00\x12&\n\"VALIDATION_TASK_TYPE_BATCH_METRICS\x10\x01\x42\x41\n\x12\x63om.tecton.dataobsP\x01Z)github.com/tecton-ai/tecton_proto/dataobs')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.dataobs.validation_task__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\022com.tecton.dataobsP\001Z)github.com/tecton-ai/tecton_proto/dataobs'
  _VALIDATIONTASK.fields_by_name['timeout']._options = None
  _VALIDATIONTASK.fields_by_name['timeout']._serialized_options = b'\030\001'
  _VALIDATIONTASKTYPE._serialized_start=1831
  _VALIDATIONTASKTYPE._serialized_end=1925
  _VALIDATIONTASK._serialized_start=381
  _VALIDATIONTASK._serialized_end=1092
  _VALIDATIONTASKRESULT._serialized_start=1095
  _VALIDATIONTASKRESULT._serialized_end=1638
  _VALIDATIONTASKMETRICS._serialized_start=1641
  _VALIDATIONTASKMETRICS._serialized_end=1829
# @@protoc_insertion_point(module_scope)
