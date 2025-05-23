# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/dataobs/metric__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)tecton_proto/dataobs/metric__client.proto\x12\x14tecton_proto.dataobs\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xdb\x02\n\x06Metric\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x1e\n\nexpression\x18\x02 \x01(\tR\nexpression\x12\x31\n\x06window\x18\x03 \x01(\x0b\x32\x19.google.protobuf.DurationR\x06window\x12\x35\n\x08interval\x18\x04 \x01(\x0b\x32\x19.google.protobuf.DurationR\x08interval\x12,\n\x12input_column_names\x18\x05 \x03(\tR\x10inputColumnNames\x12?\n\rcreation_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0c\x63reationTime\x12\x44\n\x10last_update_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0elastUpdateTime\"F\n\x0bMetricValue\x12!\n\x0c\x66\x65\x61ture_name\x18\x01 \x01(\tR\x0b\x66\x65\x61tureName\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value\"\xed\x02\n\x0fMetricDataPoint\x12J\n\x13interval_start_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x11intervalStartTime\x12\x46\n\rmetric_values\x18\x02 \x03(\x0b\x32!.tecton_proto.dataobs.MetricValueR\x0cmetricValues\x12\x34\n\x16materialization_run_id\x18\x03 \x01(\tR\x14materializationRunId\x12G\n materialization_task_attempt_url\x18\x04 \x01(\tR\x1dmaterializationTaskAttemptUrl\x12G\n\rmetric_status\x18\x05 \x01(\x0e\x32\".tecton_proto.dataobs.MetricStatusR\x0cmetricStatus\"\x96\x01\n\rFeatureMetric\x12\x41\n\x0bmetric_type\x18\x01 \x01(\x0e\x32 .tecton_proto.dataobs.MetricTypeR\nmetricType\x12!\n\x0c\x66\x65\x61ture_name\x18\x02 \x01(\tR\x0b\x66\x65\x61tureName\x12\x1f\n\x0b\x63olumn_name\x18\x03 \x01(\tR\ncolumnName*\xcb\x01\n\nMetricType\x12\x17\n\x13METRIC_TYPE_UNKNOWN\x10\x00\x12\x12\n\x0e\x43OUNT_DISTINCT\x10\x01\x12\x0e\n\nCOUNT_ROWS\x10\x02\x12\x0f\n\x0b\x43OUNT_NULLS\x10\x03\x12\x0f\n\x0b\x43OUNT_ZEROS\x10\n\x12\r\n\tAVG_VALUE\x10\x04\x12\r\n\tMAX_VALUE\x10\x05\x12\r\n\tMIN_VALUE\x10\x06\x12\x0e\n\nVAR_SAMPLE\x10\x07\x12\x11\n\rSTDDEV_SAMPLE\x10\x08\x12\x0e\n\nAVG_LENGTH\x10\t*\x8b\x01\n\x0cMetricStatus\x12\x19\n\x15METRIC_STATUS_UNKNOWN\x10\x00\x12\x1b\n\x17METRIC_STATUS_AVAILABLE\x10\x01\x12\x1d\n\x19METRIC_STATUS_UNAVAILABLE\x10\x02\x12$\n METRIC_STATUS_NO_MATERIALIZATION\x10\x03\x42\x41\n\x12\x63om.tecton.dataobsP\x01Z)github.com/tecton-ai/tecton_proto/dataobs')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.dataobs.metric__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\022com.tecton.dataobsP\001Z)github.com/tecton-ai/tecton_proto/dataobs'
  _METRICTYPE._serialized_start=1076
  _METRICTYPE._serialized_end=1279
  _METRICSTATUS._serialized_start=1282
  _METRICSTATUS._serialized_end=1421
  _METRIC._serialized_start=133
  _METRIC._serialized_end=480
  _METRICVALUE._serialized_start=482
  _METRICVALUE._serialized_end=552
  _METRICDATAPOINT._serialized_start=555
  _METRICDATAPOINT._serialized_end=920
  _FEATUREMETRIC._serialized_start=923
  _FEATUREMETRIC._serialized_end=1073
# @@protoc_insertion_point(module_scope)
