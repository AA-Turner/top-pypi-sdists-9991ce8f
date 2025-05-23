# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: yandex/cloud/mdb/kafka/v1/cluster_service.proto
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
    'yandex/cloud/mdb/kafka/v1/cluster_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.mdb.kafka.v1 import cluster_pb2 as yandex_dot_cloud_dot_mdb_dot_kafka_dot_v1_dot_cluster__pb2
from yandex.cloud.mdb.kafka.v1 import maintenance_pb2 as yandex_dot_cloud_dot_mdb_dot_kafka_dot_v1_dot_maintenance__pb2
from yandex.cloud.mdb.kafka.v1 import topic_pb2 as yandex_dot_cloud_dot_mdb_dot_kafka_dot_v1_dot_topic__pb2
from yandex.cloud.mdb.kafka.v1 import user_pb2 as yandex_dot_cloud_dot_mdb_dot_kafka_dot_v1_dot_user__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/yandex/cloud/mdb/kafka/v1/cluster_service.proto\x12\x19yandex.cloud.mdb.kafka.v1\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a yandex/cloud/api/operation.proto\x1a\'yandex/cloud/mdb/kafka/v1/cluster.proto\x1a+yandex/cloud/mdb/kafka/v1/maintenance.proto\x1a%yandex/cloud/mdb/kafka/v1/topic.proto\x1a$yandex/cloud/mdb/kafka/v1/user.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x1dyandex/cloud/validation.proto\"5\n\x11GetClusterRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\x90\x01\n\x13ListClustersRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\x12\x1a\n\x06\x66ilter\x18\x04 \x01(\tB\n\x8a\xc8\x31\x06<=1000\"e\n\x14ListClustersResponse\x12\x34\n\x08\x63lusters\x18\x01 \x03(\x0b\x32\".yandex.cloud.mdb.kafka.v1.Cluster\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\x9f\x06\n\x14\x43reateClusterRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12=\n\x04name\x18\x02 \x01(\tB/\xe8\xc7\x31\x01\xf2\xc7\x31\x1f[a-z]([-a-z0-9]{0,61}[a-z0-9])?\x8a\xc8\x31\x04\x31-63\x12\x1e\n\x0b\x64\x65scription\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x90\x01\n\x06labels\x18\x04 \x03(\x0b\x32;.yandex.cloud.mdb.kafka.v1.CreateClusterRequest.LabelsEntryBC\xf2\xc7\x31\x0f[-_./\\@0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x1c\x12\x14[a-z][-_./\\@0-9a-z]*\x1a\x04\x31-63\x12\x43\n\x0b\x65nvironment\x18\x05 \x01(\x0e\x32..yandex.cloud.mdb.kafka.v1.Cluster.Environment\x12:\n\x0b\x63onfig_spec\x18\x06 \x01(\x0b\x32%.yandex.cloud.mdb.kafka.v1.ConfigSpec\x12\x39\n\x0btopic_specs\x18\x07 \x03(\x0b\x32$.yandex.cloud.mdb.kafka.v1.TopicSpec\x12\x37\n\nuser_specs\x18\x08 \x03(\x0b\x32#.yandex.cloud.mdb.kafka.v1.UserSpec\x12\x1c\n\nnetwork_id\x18\n \x01(\tB\x08\x8a\xc8\x31\x04<=50\x12\x11\n\tsubnet_id\x18\x0b \x03(\t\x12\x1a\n\x12security_group_ids\x18\x0c \x03(\t\x12\x16\n\x0ehost_group_ids\x18\r \x03(\t\x12\x1b\n\x13\x64\x65letion_protection\x18\x0e \x01(\x08\x12H\n\x12maintenance_window\x18\x0f \x01(\x0b\x32,.yandex.cloud.mdb.kafka.v1.MaintenanceWindow\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01J\x04\x08\t\x10\n\"+\n\x15\x43reateClusterMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\"\xde\x04\n\x14UpdateClusterRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x1e\n\x0b\x64\x65scription\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x88\x01\n\x06labels\x18\x04 \x03(\x0b\x32;.yandex.cloud.mdb.kafka.v1.UpdateClusterRequest.LabelsEntryB;\xf2\xc7\x31\x0b[-_0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x18\x12\x10[a-z][-_0-9a-z]*\x1a\x04\x31-63\x12:\n\x0b\x63onfig_spec\x18\x05 \x01(\x0b\x32%.yandex.cloud.mdb.kafka.v1.ConfigSpec\x12(\n\x04name\x18\x06 \x01(\tB\x1a\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*\x8a\xc8\x31\x04<=63\x12\x1a\n\x12security_group_ids\x18\x07 \x03(\t\x12\x1b\n\x13\x64\x65letion_protection\x18\x08 \x01(\x08\x12H\n\x12maintenance_window\x18\t \x01(\x0b\x32,.yandex.cloud.mdb.kafka.v1.MaintenanceWindow\x12\x1c\n\nnetwork_id\x18\n \x01(\tB\x08\x8a\xc8\x31\x04<=50\x12\x12\n\nsubnet_ids\x18\x0b \x03(\t\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"+\n\x15UpdateClusterMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\"8\n\x14\x44\x65leteClusterRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"+\n\x15\x44\x65leteClusterMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\"\xa7\x02\n\x16ListClusterLogsRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x15\n\rcolumn_filter\x18\x02 \x03(\t\x12-\n\tfrom_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12+\n\x07to_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1d\n\tpage_size\x18\x05 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x06 \x01(\tB\t\x8a\xc8\x31\x05<=100\x12\x1e\n\x16\x61lways_next_page_token\x18\x07 \x01(\x08\x12\x1a\n\x06\x66ilter\x18\x08 \x01(\tB\n\x8a\xc8\x31\x06<=1000\"\xae\x01\n\tLogRecord\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x42\n\x07message\x18\x02 \x03(\x0b\x32\x31.yandex.cloud.mdb.kafka.v1.LogRecord.MessageEntry\x1a.\n\x0cMessageEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"f\n\x17ListClusterLogsResponse\x12\x32\n\x04logs\x18\x01 \x03(\x0b\x32$.yandex.cloud.mdb.kafka.v1.LogRecord\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"b\n\x0fStreamLogRecord\x12\x34\n\x06record\x18\x01 \x01(\x0b\x32$.yandex.cloud.mdb.kafka.v1.LogRecord\x12\x19\n\x11next_record_token\x18\x02 \x01(\t\"\xec\x01\n\x18StreamClusterLogsRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x15\n\rcolumn_filter\x18\x02 \x03(\t\x12-\n\tfrom_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12+\n\x07to_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1f\n\x0crecord_token\x18\x05 \x01(\tB\t\x8a\xc8\x31\x05<=100\x12\x1a\n\x06\x66ilter\x18\x06 \x01(\tB\n\x8a\xc8\x31\x06<=1000\"~\n\x1cListClusterOperationsRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\"o\n\x1dListClusterOperationsResponse\x12\x35\n\noperations\x18\x01 \x03(\x0b\x32!.yandex.cloud.operation.Operation\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"y\n\x17ListClusterHostsRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\"c\n\x18ListClusterHostsResponse\x12.\n\x05hosts\x18\x01 \x03(\x0b\x32\x1f.yandex.cloud.mdb.kafka.v1.Host\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"c\n\x12MoveClusterRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12+\n\x15\x64\x65stination_folder_id\x18\x02 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"b\n\x13MoveClusterMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x18\n\x10source_folder_id\x18\x02 \x01(\t\x12\x1d\n\x15\x64\x65stination_folder_id\x18\x03 \x01(\t\"7\n\x13StartClusterRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"*\n\x14StartClusterMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\"6\n\x12StopClusterRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\")\n\x13StopClusterMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\"\xca\x02\n\x1cRescheduleMaintenanceRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x65\n\x0freschedule_type\x18\x02 \x01(\x0e\x32\x46.yandex.cloud.mdb.kafka.v1.RescheduleMaintenanceRequest.RescheduleTypeB\x04\xe8\xc7\x31\x01\x12\x31\n\rdelayed_until\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"n\n\x0eRescheduleType\x12\x1f\n\x1bRESCHEDULE_TYPE_UNSPECIFIED\x10\x00\x12\r\n\tIMMEDIATE\x10\x01\x12\x19\n\x15NEXT_AVAILABLE_WINDOW\x10\x02\x12\x11\n\rSPECIFIC_TIME\x10\x03\"l\n\x1dRescheduleMaintenanceMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x31\n\rdelayed_until\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampJ\x04\x08\x02\x10\x04\x32\xa1\x12\n\x0e\x43lusterService\x12\x88\x01\n\x03Get\x12,.yandex.cloud.mdb.kafka.v1.GetClusterRequest\x1a\".yandex.cloud.mdb.kafka.v1.Cluster\"/\x82\xd3\xe4\x93\x02)\x12\'/managed-kafka/v1/clusters/{cluster_id}\x12\x8b\x01\n\x04List\x12..yandex.cloud.mdb.kafka.v1.ListClustersRequest\x1a/.yandex.cloud.mdb.kafka.v1.ListClustersResponse\"\"\x82\xd3\xe4\x93\x02\x1c\x12\x1a/managed-kafka/v1/clusters\x12\xa7\x01\n\x06\x43reate\x12/.yandex.cloud.mdb.kafka.v1.CreateClusterRequest\x1a!.yandex.cloud.operation.Operation\"I\xb2\xd2* \n\x15\x43reateClusterMetadata\x12\x07\x43luster\x82\xd3\xe4\x93\x02\x1f\"\x1a/managed-kafka/v1/clusters:\x01*\x12\xb4\x01\n\x06Update\x12/.yandex.cloud.mdb.kafka.v1.UpdateClusterRequest\x1a!.yandex.cloud.operation.Operation\"V\xb2\xd2* \n\x15UpdateClusterMetadata\x12\x07\x43luster\x82\xd3\xe4\x93\x02,2\'/managed-kafka/v1/clusters/{cluster_id}:\x01*\x12\xbf\x01\n\x06\x44\x65lete\x12/.yandex.cloud.mdb.kafka.v1.DeleteClusterRequest\x1a!.yandex.cloud.operation.Operation\"a\xb2\xd2*.\n\x15\x44\x65leteClusterMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02)*\'/managed-kafka/v1/clusters/{cluster_id}\x12\xb3\x01\n\x04Move\x12-.yandex.cloud.mdb.kafka.v1.MoveClusterRequest\x1a!.yandex.cloud.operation.Operation\"Y\xb2\xd2*\x1e\n\x13MoveClusterMetadata\x12\x07\x43luster\x82\xd3\xe4\x93\x02\x31\",/managed-kafka/v1/clusters/{cluster_id}:move:\x01*\x12\xb4\x01\n\x05Start\x12..yandex.cloud.mdb.kafka.v1.StartClusterRequest\x1a!.yandex.cloud.operation.Operation\"X\xb2\xd2*\x1f\n\x14StartClusterMetadata\x12\x07\x43luster\x82\xd3\xe4\x93\x02/\"-/managed-kafka/v1/clusters/{cluster_id}:start\x12\xb0\x01\n\x04Stop\x12-.yandex.cloud.mdb.kafka.v1.StopClusterRequest\x1a!.yandex.cloud.operation.Operation\"V\xb2\xd2*\x1e\n\x13StopClusterMetadata\x12\x07\x43luster\x82\xd3\xe4\x93\x02.\",/managed-kafka/v1/clusters/{cluster_id}:stop\x12\xe9\x01\n\x15RescheduleMaintenance\x12\x37.yandex.cloud.mdb.kafka.v1.RescheduleMaintenanceRequest\x1a!.yandex.cloud.operation.Operation\"t\xb2\xd2*(\n\x1dRescheduleMaintenanceMetadata\x12\x07\x43luster\x82\xd3\xe4\x93\x02\x42\"=/managed-kafka/v1/clusters/{cluster_id}:rescheduleMaintenance:\x01*\x12\xa7\x01\n\x08ListLogs\x12\x31.yandex.cloud.mdb.kafka.v1.ListClusterLogsRequest\x1a\x32.yandex.cloud.mdb.kafka.v1.ListClusterLogsResponse\"4\x82\xd3\xe4\x93\x02.\x12,/managed-kafka/v1/clusters/{cluster_id}:logs\x12\xac\x01\n\nStreamLogs\x12\x33.yandex.cloud.mdb.kafka.v1.StreamClusterLogsRequest\x1a*.yandex.cloud.mdb.kafka.v1.StreamLogRecord\";\x82\xd3\xe4\x93\x02\x35\x12\x33/managed-kafka/v1/clusters/{cluster_id}:stream_logs0\x01\x12\xbf\x01\n\x0eListOperations\x12\x37.yandex.cloud.mdb.kafka.v1.ListClusterOperationsRequest\x1a\x38.yandex.cloud.mdb.kafka.v1.ListClusterOperationsResponse\":\x82\xd3\xe4\x93\x02\x34\x12\x32/managed-kafka/v1/clusters/{cluster_id}/operations\x12\xab\x01\n\tListHosts\x12\x32.yandex.cloud.mdb.kafka.v1.ListClusterHostsRequest\x1a\x33.yandex.cloud.mdb.kafka.v1.ListClusterHostsResponse\"5\x82\xd3\xe4\x93\x02/\x12-/managed-kafka/v1/clusters/{cluster_id}/hostsBd\n\x1dyandex.cloud.api.mdb.kafka.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/kafka/v1;kafkab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.mdb.kafka.v1.cluster_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\035yandex.cloud.api.mdb.kafka.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/kafka/v1;kafka'
  _globals['_GETCLUSTERREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_GETCLUSTERREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTCLUSTERSREQUEST'].fields_by_name['folder_id']._loaded_options = None
  _globals['_LISTCLUSTERSREQUEST'].fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTCLUSTERSREQUEST'].fields_by_name['page_size']._loaded_options = None
  _globals['_LISTCLUSTERSREQUEST'].fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _globals['_LISTCLUSTERSREQUEST'].fields_by_name['page_token']._loaded_options = None
  _globals['_LISTCLUSTERSREQUEST'].fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _globals['_LISTCLUSTERSREQUEST'].fields_by_name['filter']._loaded_options = None
  _globals['_LISTCLUSTERSREQUEST'].fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _globals['_CREATECLUSTERREQUEST_LABELSENTRY']._loaded_options = None
  _globals['_CREATECLUSTERREQUEST_LABELSENTRY']._serialized_options = b'8\001'
  _globals['_CREATECLUSTERREQUEST'].fields_by_name['folder_id']._loaded_options = None
  _globals['_CREATECLUSTERREQUEST'].fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_CREATECLUSTERREQUEST'].fields_by_name['name']._loaded_options = None
  _globals['_CREATECLUSTERREQUEST'].fields_by_name['name']._serialized_options = b'\350\3071\001\362\3071\037[a-z]([-a-z0-9]{0,61}[a-z0-9])?\212\3101\0041-63'
  _globals['_CREATECLUSTERREQUEST'].fields_by_name['description']._loaded_options = None
  _globals['_CREATECLUSTERREQUEST'].fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _globals['_CREATECLUSTERREQUEST'].fields_by_name['labels']._loaded_options = None
  _globals['_CREATECLUSTERREQUEST'].fields_by_name['labels']._serialized_options = b'\362\3071\017[-_./\\@0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\034\022\024[a-z][-_./\\@0-9a-z]*\032\0041-63'
  _globals['_CREATECLUSTERREQUEST'].fields_by_name['network_id']._loaded_options = None
  _globals['_CREATECLUSTERREQUEST'].fields_by_name['network_id']._serialized_options = b'\212\3101\004<=50'
  _globals['_UPDATECLUSTERREQUEST_LABELSENTRY']._loaded_options = None
  _globals['_UPDATECLUSTERREQUEST_LABELSENTRY']._serialized_options = b'8\001'
  _globals['_UPDATECLUSTERREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_UPDATECLUSTERREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_UPDATECLUSTERREQUEST'].fields_by_name['description']._loaded_options = None
  _globals['_UPDATECLUSTERREQUEST'].fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _globals['_UPDATECLUSTERREQUEST'].fields_by_name['labels']._loaded_options = None
  _globals['_UPDATECLUSTERREQUEST'].fields_by_name['labels']._serialized_options = b'\362\3071\013[-_0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\030\022\020[a-z][-_0-9a-z]*\032\0041-63'
  _globals['_UPDATECLUSTERREQUEST'].fields_by_name['name']._loaded_options = None
  _globals['_UPDATECLUSTERREQUEST'].fields_by_name['name']._serialized_options = b'\362\3071\016[a-zA-Z0-9_-]*\212\3101\004<=63'
  _globals['_UPDATECLUSTERREQUEST'].fields_by_name['network_id']._loaded_options = None
  _globals['_UPDATECLUSTERREQUEST'].fields_by_name['network_id']._serialized_options = b'\212\3101\004<=50'
  _globals['_DELETECLUSTERREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_DELETECLUSTERREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTCLUSTERLOGSREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_LISTCLUSTERLOGSREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTCLUSTERLOGSREQUEST'].fields_by_name['page_size']._loaded_options = None
  _globals['_LISTCLUSTERLOGSREQUEST'].fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _globals['_LISTCLUSTERLOGSREQUEST'].fields_by_name['page_token']._loaded_options = None
  _globals['_LISTCLUSTERLOGSREQUEST'].fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _globals['_LISTCLUSTERLOGSREQUEST'].fields_by_name['filter']._loaded_options = None
  _globals['_LISTCLUSTERLOGSREQUEST'].fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _globals['_LOGRECORD_MESSAGEENTRY']._loaded_options = None
  _globals['_LOGRECORD_MESSAGEENTRY']._serialized_options = b'8\001'
  _globals['_STREAMCLUSTERLOGSREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_STREAMCLUSTERLOGSREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_STREAMCLUSTERLOGSREQUEST'].fields_by_name['record_token']._loaded_options = None
  _globals['_STREAMCLUSTERLOGSREQUEST'].fields_by_name['record_token']._serialized_options = b'\212\3101\005<=100'
  _globals['_STREAMCLUSTERLOGSREQUEST'].fields_by_name['filter']._loaded_options = None
  _globals['_STREAMCLUSTERLOGSREQUEST'].fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _globals['_LISTCLUSTEROPERATIONSREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_LISTCLUSTEROPERATIONSREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTCLUSTEROPERATIONSREQUEST'].fields_by_name['page_size']._loaded_options = None
  _globals['_LISTCLUSTEROPERATIONSREQUEST'].fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _globals['_LISTCLUSTEROPERATIONSREQUEST'].fields_by_name['page_token']._loaded_options = None
  _globals['_LISTCLUSTEROPERATIONSREQUEST'].fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _globals['_LISTCLUSTERHOSTSREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_LISTCLUSTERHOSTSREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTCLUSTERHOSTSREQUEST'].fields_by_name['page_size']._loaded_options = None
  _globals['_LISTCLUSTERHOSTSREQUEST'].fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _globals['_LISTCLUSTERHOSTSREQUEST'].fields_by_name['page_token']._loaded_options = None
  _globals['_LISTCLUSTERHOSTSREQUEST'].fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _globals['_MOVECLUSTERREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_MOVECLUSTERREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_MOVECLUSTERREQUEST'].fields_by_name['destination_folder_id']._loaded_options = None
  _globals['_MOVECLUSTERREQUEST'].fields_by_name['destination_folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_STARTCLUSTERREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_STARTCLUSTERREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_STOPCLUSTERREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_STOPCLUSTERREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_RESCHEDULEMAINTENANCEREQUEST'].fields_by_name['cluster_id']._loaded_options = None
  _globals['_RESCHEDULEMAINTENANCEREQUEST'].fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_RESCHEDULEMAINTENANCEREQUEST'].fields_by_name['reschedule_type']._loaded_options = None
  _globals['_RESCHEDULEMAINTENANCEREQUEST'].fields_by_name['reschedule_type']._serialized_options = b'\350\3071\001'
  _globals['_CLUSTERSERVICE'].methods_by_name['Get']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['Get']._serialized_options = b'\202\323\344\223\002)\022\'/managed-kafka/v1/clusters/{cluster_id}'
  _globals['_CLUSTERSERVICE'].methods_by_name['List']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['List']._serialized_options = b'\202\323\344\223\002\034\022\032/managed-kafka/v1/clusters'
  _globals['_CLUSTERSERVICE'].methods_by_name['Create']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['Create']._serialized_options = b'\262\322* \n\025CreateClusterMetadata\022\007Cluster\202\323\344\223\002\037\"\032/managed-kafka/v1/clusters:\001*'
  _globals['_CLUSTERSERVICE'].methods_by_name['Update']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['Update']._serialized_options = b'\262\322* \n\025UpdateClusterMetadata\022\007Cluster\202\323\344\223\002,2\'/managed-kafka/v1/clusters/{cluster_id}:\001*'
  _globals['_CLUSTERSERVICE'].methods_by_name['Delete']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['Delete']._serialized_options = b'\262\322*.\n\025DeleteClusterMetadata\022\025google.protobuf.Empty\202\323\344\223\002)*\'/managed-kafka/v1/clusters/{cluster_id}'
  _globals['_CLUSTERSERVICE'].methods_by_name['Move']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['Move']._serialized_options = b'\262\322*\036\n\023MoveClusterMetadata\022\007Cluster\202\323\344\223\0021\",/managed-kafka/v1/clusters/{cluster_id}:move:\001*'
  _globals['_CLUSTERSERVICE'].methods_by_name['Start']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['Start']._serialized_options = b'\262\322*\037\n\024StartClusterMetadata\022\007Cluster\202\323\344\223\002/\"-/managed-kafka/v1/clusters/{cluster_id}:start'
  _globals['_CLUSTERSERVICE'].methods_by_name['Stop']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['Stop']._serialized_options = b'\262\322*\036\n\023StopClusterMetadata\022\007Cluster\202\323\344\223\002.\",/managed-kafka/v1/clusters/{cluster_id}:stop'
  _globals['_CLUSTERSERVICE'].methods_by_name['RescheduleMaintenance']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['RescheduleMaintenance']._serialized_options = b'\262\322*(\n\035RescheduleMaintenanceMetadata\022\007Cluster\202\323\344\223\002B\"=/managed-kafka/v1/clusters/{cluster_id}:rescheduleMaintenance:\001*'
  _globals['_CLUSTERSERVICE'].methods_by_name['ListLogs']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['ListLogs']._serialized_options = b'\202\323\344\223\002.\022,/managed-kafka/v1/clusters/{cluster_id}:logs'
  _globals['_CLUSTERSERVICE'].methods_by_name['StreamLogs']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['StreamLogs']._serialized_options = b'\202\323\344\223\0025\0223/managed-kafka/v1/clusters/{cluster_id}:stream_logs'
  _globals['_CLUSTERSERVICE'].methods_by_name['ListOperations']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['ListOperations']._serialized_options = b'\202\323\344\223\0024\0222/managed-kafka/v1/clusters/{cluster_id}/operations'
  _globals['_CLUSTERSERVICE'].methods_by_name['ListHosts']._loaded_options = None
  _globals['_CLUSTERSERVICE'].methods_by_name['ListHosts']._serialized_options = b'\202\323\344\223\002/\022-/managed-kafka/v1/clusters/{cluster_id}/hosts'
  _globals['_GETCLUSTERREQUEST']._serialized_start=443
  _globals['_GETCLUSTERREQUEST']._serialized_end=496
  _globals['_LISTCLUSTERSREQUEST']._serialized_start=499
  _globals['_LISTCLUSTERSREQUEST']._serialized_end=643
  _globals['_LISTCLUSTERSRESPONSE']._serialized_start=645
  _globals['_LISTCLUSTERSRESPONSE']._serialized_end=746
  _globals['_CREATECLUSTERREQUEST']._serialized_start=749
  _globals['_CREATECLUSTERREQUEST']._serialized_end=1548
  _globals['_CREATECLUSTERREQUEST_LABELSENTRY']._serialized_start=1497
  _globals['_CREATECLUSTERREQUEST_LABELSENTRY']._serialized_end=1542
  _globals['_CREATECLUSTERMETADATA']._serialized_start=1550
  _globals['_CREATECLUSTERMETADATA']._serialized_end=1593
  _globals['_UPDATECLUSTERREQUEST']._serialized_start=1596
  _globals['_UPDATECLUSTERREQUEST']._serialized_end=2202
  _globals['_UPDATECLUSTERREQUEST_LABELSENTRY']._serialized_start=1497
  _globals['_UPDATECLUSTERREQUEST_LABELSENTRY']._serialized_end=1542
  _globals['_UPDATECLUSTERMETADATA']._serialized_start=2204
  _globals['_UPDATECLUSTERMETADATA']._serialized_end=2247
  _globals['_DELETECLUSTERREQUEST']._serialized_start=2249
  _globals['_DELETECLUSTERREQUEST']._serialized_end=2305
  _globals['_DELETECLUSTERMETADATA']._serialized_start=2307
  _globals['_DELETECLUSTERMETADATA']._serialized_end=2350
  _globals['_LISTCLUSTERLOGSREQUEST']._serialized_start=2353
  _globals['_LISTCLUSTERLOGSREQUEST']._serialized_end=2648
  _globals['_LOGRECORD']._serialized_start=2651
  _globals['_LOGRECORD']._serialized_end=2825
  _globals['_LOGRECORD_MESSAGEENTRY']._serialized_start=2779
  _globals['_LOGRECORD_MESSAGEENTRY']._serialized_end=2825
  _globals['_LISTCLUSTERLOGSRESPONSE']._serialized_start=2827
  _globals['_LISTCLUSTERLOGSRESPONSE']._serialized_end=2929
  _globals['_STREAMLOGRECORD']._serialized_start=2931
  _globals['_STREAMLOGRECORD']._serialized_end=3029
  _globals['_STREAMCLUSTERLOGSREQUEST']._serialized_start=3032
  _globals['_STREAMCLUSTERLOGSREQUEST']._serialized_end=3268
  _globals['_LISTCLUSTEROPERATIONSREQUEST']._serialized_start=3270
  _globals['_LISTCLUSTEROPERATIONSREQUEST']._serialized_end=3396
  _globals['_LISTCLUSTEROPERATIONSRESPONSE']._serialized_start=3398
  _globals['_LISTCLUSTEROPERATIONSRESPONSE']._serialized_end=3509
  _globals['_LISTCLUSTERHOSTSREQUEST']._serialized_start=3511
  _globals['_LISTCLUSTERHOSTSREQUEST']._serialized_end=3632
  _globals['_LISTCLUSTERHOSTSRESPONSE']._serialized_start=3634
  _globals['_LISTCLUSTERHOSTSRESPONSE']._serialized_end=3733
  _globals['_MOVECLUSTERREQUEST']._serialized_start=3735
  _globals['_MOVECLUSTERREQUEST']._serialized_end=3834
  _globals['_MOVECLUSTERMETADATA']._serialized_start=3836
  _globals['_MOVECLUSTERMETADATA']._serialized_end=3934
  _globals['_STARTCLUSTERREQUEST']._serialized_start=3936
  _globals['_STARTCLUSTERREQUEST']._serialized_end=3991
  _globals['_STARTCLUSTERMETADATA']._serialized_start=3993
  _globals['_STARTCLUSTERMETADATA']._serialized_end=4035
  _globals['_STOPCLUSTERREQUEST']._serialized_start=4037
  _globals['_STOPCLUSTERREQUEST']._serialized_end=4091
  _globals['_STOPCLUSTERMETADATA']._serialized_start=4093
  _globals['_STOPCLUSTERMETADATA']._serialized_end=4134
  _globals['_RESCHEDULEMAINTENANCEREQUEST']._serialized_start=4137
  _globals['_RESCHEDULEMAINTENANCEREQUEST']._serialized_end=4467
  _globals['_RESCHEDULEMAINTENANCEREQUEST_RESCHEDULETYPE']._serialized_start=4357
  _globals['_RESCHEDULEMAINTENANCEREQUEST_RESCHEDULETYPE']._serialized_end=4467
  _globals['_RESCHEDULEMAINTENANCEMETADATA']._serialized_start=4469
  _globals['_RESCHEDULEMAINTENANCEMETADATA']._serialized_end=4577
  _globals['_CLUSTERSERVICE']._serialized_start=4580
  _globals['_CLUSTERSERVICE']._serialized_end=6917
# @@protoc_insertion_point(module_scope)
