# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud.trino.v1 import catalog_pb2 as yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__pb2
from yandex.cloud.trino.v1 import catalog_service_pb2 as yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in yandex/cloud/trino/v1/catalog_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class CatalogServiceStub(object):
    """A set of methods for managing Trino Cluster Catalog resources.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/yandex.cloud.trino.v1.CatalogService/Get',
                request_serializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.GetCatalogRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__pb2.Catalog.FromString,
                _registered_method=True)
        self.List = channel.unary_unary(
                '/yandex.cloud.trino.v1.CatalogService/List',
                request_serializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.ListCatalogsRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.ListCatalogsResponse.FromString,
                _registered_method=True)
        self.Create = channel.unary_unary(
                '/yandex.cloud.trino.v1.CatalogService/Create',
                request_serializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.CreateCatalogRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                _registered_method=True)
        self.Update = channel.unary_unary(
                '/yandex.cloud.trino.v1.CatalogService/Update',
                request_serializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.UpdateCatalogRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                _registered_method=True)
        self.Delete = channel.unary_unary(
                '/yandex.cloud.trino.v1.CatalogService/Delete',
                request_serializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.DeleteCatalogRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                _registered_method=True)


class CatalogServiceServicer(object):
    """A set of methods for managing Trino Cluster Catalog resources.
    """

    def Get(self, request, context):
        """Returns the specified Trino Catalog resource.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """Retrieves a list of Trino Catalog resources.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Creates a new Trino Catalog.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Update(self, request, context):
        """Updates the specified Trino Catalog.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Deletes the specified Trino Catalog.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CatalogServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.GetCatalogRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__pb2.Catalog.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.ListCatalogsRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.ListCatalogsResponse.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.CreateCatalogRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.UpdateCatalogRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.DeleteCatalogRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'yandex.cloud.trino.v1.CatalogService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('yandex.cloud.trino.v1.CatalogService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class CatalogService(object):
    """A set of methods for managing Trino Cluster Catalog resources.
    """

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/yandex.cloud.trino.v1.CatalogService/Get',
            yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.GetCatalogRequest.SerializeToString,
            yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__pb2.Catalog.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/yandex.cloud.trino.v1.CatalogService/List',
            yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.ListCatalogsRequest.SerializeToString,
            yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.ListCatalogsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/yandex.cloud.trino.v1.CatalogService/Create',
            yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.CreateCatalogRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/yandex.cloud.trino.v1.CatalogService/Update',
            yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.UpdateCatalogRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/yandex.cloud.trino.v1.CatalogService/Delete',
            yandex_dot_cloud_dot_trino_dot_v1_dot_catalog__service__pb2.DeleteCatalogRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
