# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/remote_spark__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.args import data_source_config__client_pb2 as tecton__proto_dot_args_dot_data__source__config____client__pb2
from tecton_proto.args import feature_view__client_pb2 as tecton__proto_dot_args_dot_feature__view____client__pb2
from tecton_proto.args import user_defined_function__client_pb2 as tecton__proto_dot_args_dot_user__defined__function____client__pb2
from tecton_proto.args import virtual_data_source__client_pb2 as tecton__proto_dot_args_dot_virtual__data__source____client__pb2
from tecton_proto.common import schema__client_pb2 as tecton__proto_dot_common_dot_schema____client__pb2
from tecton_proto.common import spark_schema__client_pb2 as tecton__proto_dot_common_dot_spark__schema____client__pb2
from tecton_proto.data import feature_view__client_pb2 as tecton__proto_dot_data_dot_feature__view____client__pb2
from tecton_proto.data import hive_metastore__client_pb2 as tecton__proto_dot_data_dot_hive__metastore____client__pb2
from tecton_proto.data import transformation__client_pb2 as tecton__proto_dot_data_dot_transformation____client__pb2
from tecton_proto.data import virtual_data_source__client_pb2 as tecton__proto_dot_data_dot_virtual__data__source____client__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,tecton_proto/data/remote_spark__client.proto\x12\x11tecton_proto.data\x1a\x32tecton_proto/args/data_source_config__client.proto\x1a,tecton_proto/args/feature_view__client.proto\x1a\x35tecton_proto/args/user_defined_function__client.proto\x1a\x33tecton_proto/args/virtual_data_source__client.proto\x1a(tecton_proto/common/schema__client.proto\x1a.tecton_proto/common/spark_schema__client.proto\x1a,tecton_proto/data/feature_view__client.proto\x1a.tecton_proto/data/hive_metastore__client.proto\x1a.tecton_proto/data/transformation__client.proto\x1a\x33tecton_proto/data/virtual_data_source__client.proto\"\xf2\x01\n\x12GetHiveTableSchema\x12\x1a\n\x08\x64\x61tabase\x18\x01 \x01(\tR\x08\x64\x61tabase\x12\x14\n\x05table\x18\x02 \x01(\tR\x05table\x12(\n\x0ftimestampColumn\x18\x03 \x01(\tR\x0ftimestampColumn\x12(\n\x0ftimestampFormat\x18\x04 \x01(\tR\x0ftimestampFormat\x12V\n\x12rawBatchTranslator\x18\x05 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\x12rawBatchTranslator\"\x89\x02\n\x13GetUnityTableSchema\x12\x18\n\x07\x63\x61talog\x18\x01 \x01(\tR\x07\x63\x61talog\x12\x16\n\x06schema\x18\x02 \x01(\tR\x06schema\x12\x14\n\x05table\x18\x03 \x01(\tR\x05table\x12(\n\x0ftimestampColumn\x18\x04 \x01(\tR\x0ftimestampColumn\x12(\n\x0ftimestampFormat\x18\x05 \x01(\tR\x0ftimestampFormat\x12V\n\x12rawBatchTranslator\x18\x06 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\x12rawBatchTranslator\"\x9e\x01\n GetBatchDataSourceFunctionSchema\x12\x42\n\x08\x66unction\x18\x01 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\x08\x66unction\x12\x36\n\x17supports_time_filtering\x18\x02 \x01(\x08R\x15supportsTimeFiltering\"g\n!GetStreamDataSourceFunctionSchema\x12\x42\n\x08\x66unction\x18\x01 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\x08\x66unction\"\xd8\x01\n\x16GetRedshiftTableSchema\x12\x1a\n\x08\x65ndpoint\x18\x01 \x01(\tR\x08\x65ndpoint\x12\x14\n\x05table\x18\x02 \x01(\tR\x05table\x12\x14\n\x05query\x18\x03 \x01(\tR\x05query\x12V\n\x12rawBatchTranslator\x18\x04 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\x12rawBatchTranslator\x12\x1e\n\x0btemp_s3_dir\x18\x05 \x01(\tR\ttempS3Dir\"\x95\x02\n\x12GetSnowflakeSchema\x12\x10\n\x03url\x18\x01 \x01(\tR\x03url\x12\x12\n\x04role\x18\x02 \x01(\tR\x04role\x12\x1a\n\x08\x64\x61tabase\x18\x03 \x01(\tR\x08\x64\x61tabase\x12\x16\n\x06schema\x18\x04 \x01(\tR\x06schema\x12\x1c\n\twarehouse\x18\x05 \x01(\tR\twarehouse\x12\x16\n\x05table\x18\x06 \x01(\tH\x00R\x05table\x12\x16\n\x05query\x18\x07 \x01(\tH\x00R\x05query\x12M\n\x0epost_processor\x18\x08 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\rpostProcessorB\x08\n\x06source\"\x8d\x03\n\x13GetFileSourceSchema\x12\x10\n\x03uri\x18\x01 \x01(\tR\x03uri\x12\x1e\n\nfileFormat\x18\x02 \x01(\tR\nfileFormat\x12\x30\n\x13\x63onvertToGlueFormat\x18\x03 \x01(\x08R\x13\x63onvertToGlueFormat\x12V\n\x12rawBatchTranslator\x18\x04 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\x12rawBatchTranslator\x12\x1c\n\tschemaUri\x18\x05 \x01(\tR\tschemaUri\x12(\n\x0ftimestampColumn\x18\x06 \x01(\tR\x0ftimestampColumn\x12(\n\x0ftimestampFormat\x18\x07 \x01(\tR\x0ftimestampFormat\x12H\n\x0eschemaOverride\x18\x08 \x01(\x0b\x32 .tecton_proto.common.SparkSchemaR\x0eschemaOverride\"\x92\x01\n\x16GetKinesisSourceSchema\x12\x1e\n\nstreamName\x18\x01 \x01(\tR\nstreamName\x12X\n\x13rawStreamTranslator\x18\x02 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\x13rawStreamTranslator\"\xea\x01\n\x14GetKafkaSourceSchema\x12X\n\x13rawStreamTranslator\x18\x01 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\x13rawStreamTranslator\x12\x32\n\x15ssl_keystore_location\x18\x02 \x01(\tR\x13sslKeystoreLocation\x12\x44\n\x1fssl_keystore_password_secret_id\x18\x03 \x01(\tR\x1bsslKeystorePasswordSecretId\"\x8e\x02\n\x14GetFeatureViewSchema\x12V\n\x14virtual_data_sources\x18\x02 \x03(\x0b\x32$.tecton_proto.data.VirtualDataSourceR\x12virtualDataSources\x12K\n\x0ftransformations\x18\x03 \x03(\x0b\x32!.tecton_proto.data.TransformationR\x0ftransformations\x12\x45\n\x0c\x66\x65\x61ture_view\x18\x05 \x01(\x0b\x32\".tecton_proto.args.FeatureViewArgsR\x0b\x66\x65\x61tureViewJ\x04\x08\x01\x10\x02J\x04\x08\x04\x10\x05\"\x9a\x02\n&GetQueryPlanInfoForFeatureViewPipeline\x12V\n\x14virtual_data_sources\x18\x02 \x03(\x0b\x32$.tecton_proto.data.VirtualDataSourceR\x12virtualDataSources\x12K\n\x0ftransformations\x18\x03 \x03(\x0b\x32!.tecton_proto.data.TransformationR\x0ftransformations\x12\x45\n\x0c\x66\x65\x61ture_view\x18\x04 \x01(\x0b\x32\".tecton_proto.args.FeatureViewArgsR\x0b\x66\x65\x61tureViewJ\x04\x08\x01\x10\x02\"\x13\n\x11ListHiveDatabases\",\n\x0eListHiveTables\x12\x1a\n\x08\x64\x61tabase\x18\x01 \x01(\tR\x08\x64\x61tabase\"H\n\x14ListHiveTableColumns\x12\x1a\n\x08\x64\x61tabase\x18\x01 \x01(\tR\x08\x64\x61tabase\x12\x14\n\x05table\x18\x02 \x01(\tR\x05table\"\xd3\x01\n\x18\x46\x65\x61tureViewSchemaRequest\x12\x45\n\x0c\x66\x65\x61ture_view\x18\x01 \x01(\x0b\x32\".tecton_proto.args.FeatureViewArgsR\x0b\x66\x65\x61tureView\x12\x1b\n\tjoin_keys\x18\x02 \x03(\tR\x08joinKeys\x12S\n\x12temporal_aggregate\x18\x03 \x01(\x0b\x32$.tecton_proto.data.TemporalAggregateR\x11temporalAggregate\"\xac\x02\n$GetMultipleFeatureViewSchemasRequest\x12V\n\x14virtual_data_sources\x18\x01 \x03(\x0b\x32$.tecton_proto.data.VirtualDataSourceR\x12virtualDataSources\x12K\n\x0ftransformations\x18\x02 \x03(\x0b\x32!.tecton_proto.data.TransformationR\x0ftransformations\x12_\n\x15\x66\x65\x61ture_view_requests\x18\x03 \x03(\x0b\x32+.tecton_proto.data.FeatureViewSchemaRequestR\x13\x66\x65\x61tureViewRequests\"\xa9\x02\n%GetMultipleFeatureViewSchemasResponse\x12\x88\x01\n\x16\x66\x65\x61ture_view_responses\x18\x01 \x03(\x0b\x32R.tecton_proto.data.GetMultipleFeatureViewSchemasResponse.FeatureViewResponsesEntryR\x14\x66\x65\x61tureViewResponses\x1au\n\x19\x46\x65\x61tureViewResponsesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x42\n\x05value\x18\x02 \x01(\x0b\x32,.tecton_proto.data.FeatureViewSchemaResponseR\x05value:\x02\x38\x01\"y\n#GetMultipleDataSourceSchemasRequest\x12R\n\x10\x64\x61ta_source_args\x18\x01 \x03(\x0b\x32(.tecton_proto.args.VirtualDataSourceArgsR\x0e\x64\x61taSourceArgs\"\x96\x02\n$GetMultipleDataSourceSchemasResponse\x12\x84\x01\n\x15\x64\x61ta_source_responses\x18\x01 \x03(\x0b\x32P.tecton_proto.data.GetMultipleDataSourceSchemasResponse.DataSourceResponsesEntryR\x13\x64\x61taSourceResponses\x1ag\n\x18\x44\x61taSourceResponsesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1f.tecton_proto.data.SparkSchemasR\x05value:\x02\x38\x01\"\x98\x01\n\x0cSparkSchemas\x12\x42\n\x0b\x62\x61tchSchema\x18\x01 \x01(\x0b\x32 .tecton_proto.common.SparkSchemaR\x0b\x62\x61tchSchema\x12\x44\n\x0cstreamSchema\x18\x02 \x01(\x0b\x32 .tecton_proto.common.SparkSchemaR\x0cstreamSchema\"~\n\x19\x46\x65\x61tureViewSchemaResponse\x12<\n\x0bview_schema\x18\x01 \x01(\x0b\x32\x1b.tecton_proto.common.SchemaR\nviewSchema\x12#\n\rtimestamp_key\x18\x03 \x01(\tR\x0ctimestampKey\"\xfd\x0e\n\x0e\x45xecuteRequest\x12\x8d\x01\n$getMultipleFeatureViewSchemasRequest\x18\x18 \x01(\x0b\x32\x37.tecton_proto.data.GetMultipleFeatureViewSchemasRequestH\x00R$getMultipleFeatureViewSchemasRequest\x12\x8a\x01\n#getMultipleDataSourceSchemasRequest\x18\x19 \x01(\x0b\x32\x36.tecton_proto.data.GetMultipleDataSourceSchemasRequestH\x00R#getMultipleDataSourceSchemasRequest\x12W\n\x12getHiveTableSchema\x18\x01 \x01(\x0b\x32%.tecton_proto.data.GetHiveTableSchemaH\x00R\x12getHiveTableSchema\x12\x63\n\x16getRedshiftTableSchema\x18\x02 \x01(\x0b\x32).tecton_proto.data.GetRedshiftTableSchemaH\x00R\x16getRedshiftTableSchema\x12Z\n\x13getFileSourceSchema\x18\x03 \x01(\x0b\x32&.tecton_proto.data.GetFileSourceSchemaH\x00R\x13getFileSourceSchema\x12\x63\n\x16getKinesisSourceSchema\x18\x04 \x01(\x0b\x32).tecton_proto.data.GetKinesisSourceSchemaH\x00R\x16getKinesisSourceSchema\x12]\n\x14getKafkaSourceSchema\x18\x05 \x01(\x0b\x32\'.tecton_proto.data.GetKafkaSourceSchemaH\x00R\x14getKafkaSourceSchema\x12]\n\x14getFeatureViewSchema\x18\x0e \x01(\x0b\x32\'.tecton_proto.data.GetFeatureViewSchemaH\x00R\x14getFeatureViewSchema\x12W\n\x12getSnowflakeSchema\x18\x0c \x01(\x0b\x32%.tecton_proto.data.GetSnowflakeSchemaH\x00R\x12getSnowflakeSchema\x12\x81\x01\n getBatchDataSourceFunctionSchema\x18\x15 \x01(\x0b\x32\x33.tecton_proto.data.GetBatchDataSourceFunctionSchemaH\x00R getBatchDataSourceFunctionSchema\x12\x84\x01\n!getStreamDataSourceFunctionSchema\x18\x16 \x01(\x0b\x32\x34.tecton_proto.data.GetStreamDataSourceFunctionSchemaH\x00R!getStreamDataSourceFunctionSchema\x12Z\n\x13getUnityTableSchema\x18\x17 \x01(\x0b\x32&.tecton_proto.data.GetUnityTableSchemaH\x00R\x13getUnityTableSchema\x12T\n\x11listHiveDatabases\x18\x12 \x01(\x0b\x32$.tecton_proto.data.ListHiveDatabasesH\x00R\x11listHiveDatabases\x12K\n\x0elistHiveTables\x18\x13 \x01(\x0b\x32!.tecton_proto.data.ListHiveTablesH\x00R\x0elistHiveTables\x12]\n\x14listHiveTableColumns\x18\x14 \x01(\x0b\x32\'.tecton_proto.data.ListHiveTableColumnsH\x00R\x14listHiveTableColumns\x12\x93\x01\n&getQueryPlanInfoForFeatureViewPipeline\x18\r \x01(\x0b\x32\x39.tecton_proto.data.GetQueryPlanInfoForFeatureViewPipelineH\x00R&getQueryPlanInfoForFeatureViewPipeline\x12H\n\x07\x65nvVars\x18\x10 \x03(\x0b\x32..tecton_proto.data.ExecuteRequest.EnvVarsEntryR\x07\x65nvVars\x1a:\n\x0c\x45nvVarsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\t\n\x07requestJ\x04\x08\x06\x10\x07J\x04\x08\x07\x10\x08J\x04\x08\x08\x10\tJ\x04\x08\t\x10\nJ\x04\x08\n\x10\x0bJ\x04\x08\x0b\x10\x0cJ\x04\x08\x11\x10\x12\"]\n\rQueryPlanInfo\x12\x1b\n\thas_joins\x18\x01 \x01(\x08R\x08hasJoins\x12)\n\x10has_aggregations\x18\x02 \x01(\x08R\x0fhasAggregationsJ\x04\x08\x03\x10\x04\"\x94\x05\n\rExecuteResult\x12&\n\runcaughtError\x18\x01 \x01(\tH\x00R\runcaughtError\x12*\n\x0fvalidationError\x18\x05 \x01(\tH\x00R\x0fvalidationError\x12\x44\n\x0bsparkSchema\x18\x02 \x01(\x0b\x32 .tecton_proto.common.SparkSchemaH\x00R\x0bsparkSchema\x12H\n\rqueryPlanInfo\x18\x03 \x01(\x0b\x32 .tecton_proto.data.QueryPlanInfoH\x00R\rqueryPlanInfo\x12\x35\n\x06schema\x18\x04 \x01(\x0b\x32\x1b.tecton_proto.common.SchemaH\x00R\x06schema\x12K\n\x0elistHiveResult\x18\x06 \x01(\x0b\x32!.tecton_proto.data.ListHiveResultH\x00R\x0elistHiveResult\x12\x88\x01\n!multipleFeatureViewSchemaResponse\x18\x08 \x01(\x0b\x32\x38.tecton_proto.data.GetMultipleFeatureViewSchemasResponseH\x00R!multipleFeatureViewSchemaResponse\x12\x85\x01\n multipleDataSourceSchemaResponse\x18\t \x01(\x0b\x32\x37.tecton_proto.data.GetMultipleDataSourceSchemasResponseH\x00R multipleDataSourceSchemaResponseB\x08\n\x06resultB;\n\x0f\x63om.tecton.dataP\x01Z&github.com/tecton-ai/tecton_proto/data')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.remote_spark__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001Z&github.com/tecton-ai/tecton_proto/data'
  _GETMULTIPLEFEATUREVIEWSCHEMASRESPONSE_FEATUREVIEWRESPONSESENTRY._options = None
  _GETMULTIPLEFEATUREVIEWSCHEMASRESPONSE_FEATUREVIEWRESPONSESENTRY._serialized_options = b'8\001'
  _GETMULTIPLEDATASOURCESCHEMASRESPONSE_DATASOURCERESPONSESENTRY._options = None
  _GETMULTIPLEDATASOURCESCHEMASRESPONSE_DATASOURCERESPONSESENTRY._serialized_options = b'8\001'
  _EXECUTEREQUEST_ENVVARSENTRY._options = None
  _EXECUTEREQUEST_ENVVARSENTRY._serialized_options = b'8\001'
  _GETHIVETABLESCHEMA._serialized_start=559
  _GETHIVETABLESCHEMA._serialized_end=801
  _GETUNITYTABLESCHEMA._serialized_start=804
  _GETUNITYTABLESCHEMA._serialized_end=1069
  _GETBATCHDATASOURCEFUNCTIONSCHEMA._serialized_start=1072
  _GETBATCHDATASOURCEFUNCTIONSCHEMA._serialized_end=1230
  _GETSTREAMDATASOURCEFUNCTIONSCHEMA._serialized_start=1232
  _GETSTREAMDATASOURCEFUNCTIONSCHEMA._serialized_end=1335
  _GETREDSHIFTTABLESCHEMA._serialized_start=1338
  _GETREDSHIFTTABLESCHEMA._serialized_end=1554
  _GETSNOWFLAKESCHEMA._serialized_start=1557
  _GETSNOWFLAKESCHEMA._serialized_end=1834
  _GETFILESOURCESCHEMA._serialized_start=1837
  _GETFILESOURCESCHEMA._serialized_end=2234
  _GETKINESISSOURCESCHEMA._serialized_start=2237
  _GETKINESISSOURCESCHEMA._serialized_end=2383
  _GETKAFKASOURCESCHEMA._serialized_start=2386
  _GETKAFKASOURCESCHEMA._serialized_end=2620
  _GETFEATUREVIEWSCHEMA._serialized_start=2623
  _GETFEATUREVIEWSCHEMA._serialized_end=2893
  _GETQUERYPLANINFOFORFEATUREVIEWPIPELINE._serialized_start=2896
  _GETQUERYPLANINFOFORFEATUREVIEWPIPELINE._serialized_end=3178
  _LISTHIVEDATABASES._serialized_start=3180
  _LISTHIVEDATABASES._serialized_end=3199
  _LISTHIVETABLES._serialized_start=3201
  _LISTHIVETABLES._serialized_end=3245
  _LISTHIVETABLECOLUMNS._serialized_start=3247
  _LISTHIVETABLECOLUMNS._serialized_end=3319
  _FEATUREVIEWSCHEMAREQUEST._serialized_start=3322
  _FEATUREVIEWSCHEMAREQUEST._serialized_end=3533
  _GETMULTIPLEFEATUREVIEWSCHEMASREQUEST._serialized_start=3536
  _GETMULTIPLEFEATUREVIEWSCHEMASREQUEST._serialized_end=3836
  _GETMULTIPLEFEATUREVIEWSCHEMASRESPONSE._serialized_start=3839
  _GETMULTIPLEFEATUREVIEWSCHEMASRESPONSE._serialized_end=4136
  _GETMULTIPLEFEATUREVIEWSCHEMASRESPONSE_FEATUREVIEWRESPONSESENTRY._serialized_start=4019
  _GETMULTIPLEFEATUREVIEWSCHEMASRESPONSE_FEATUREVIEWRESPONSESENTRY._serialized_end=4136
  _GETMULTIPLEDATASOURCESCHEMASREQUEST._serialized_start=4138
  _GETMULTIPLEDATASOURCESCHEMASREQUEST._serialized_end=4259
  _GETMULTIPLEDATASOURCESCHEMASRESPONSE._serialized_start=4262
  _GETMULTIPLEDATASOURCESCHEMASRESPONSE._serialized_end=4540
  _GETMULTIPLEDATASOURCESCHEMASRESPONSE_DATASOURCERESPONSESENTRY._serialized_start=4437
  _GETMULTIPLEDATASOURCESCHEMASRESPONSE_DATASOURCERESPONSESENTRY._serialized_end=4540
  _SPARKSCHEMAS._serialized_start=4543
  _SPARKSCHEMAS._serialized_end=4695
  _FEATUREVIEWSCHEMARESPONSE._serialized_start=4697
  _FEATUREVIEWSCHEMARESPONSE._serialized_end=4823
  _EXECUTEREQUEST._serialized_start=4826
  _EXECUTEREQUEST._serialized_end=6743
  _EXECUTEREQUEST_ENVVARSENTRY._serialized_start=6632
  _EXECUTEREQUEST_ENVVARSENTRY._serialized_end=6690
  _QUERYPLANINFO._serialized_start=6745
  _QUERYPLANINFO._serialized_end=6838
  _EXECUTERESULT._serialized_start=6841
  _EXECUTERESULT._serialized_end=7501
# @@protoc_insertion_point(module_scope)
