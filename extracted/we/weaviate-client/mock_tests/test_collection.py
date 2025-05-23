import datetime
from typing import Any, Dict, Literal

import grpc
import pytest
from pytest_httpserver import HTTPServer

import weaviate
import weaviate.classes as wvc
from mock_tests.conftest import (
    MOCK_IP,
    MOCK_PORT,
    MOCK_PORT_GRPC,
    MockRetriesWeaviateService,
)
from weaviate.backup.backup import BackupStorage
from weaviate.collections.classes.config import (
    BM25Config,
    CollectionConfig,
    InvertedIndexConfig,
    MultiTenancyConfig,
    ReplicationConfig,
    ReplicationDeletionStrategy,
    ShardingConfig,
    StopwordsConfig,
    StopwordsPreset,
    VectorDistances,
    VectorIndexConfigFlat,
    VectorIndexType,
    Vectorizers,
)
from weaviate.connect.base import ConnectionParams, ProtocolParams
from weaviate.connect.integrations import _IntegrationConfig
from weaviate.exceptions import (
    BackupCanceledError,
    InsufficientPermissionsError,
    UnexpectedStatusCodeError,
    WeaviateStartUpError,
)

ACCESS_TOKEN = "HELLO!IamAnAccessToken"
REFRESH_TOKEN = "UseMeToRefreshYourAccessToken"


def test_insufficient_permissions(
    weaviate_mock: HTTPServer, start_grpc_server: grpc.Server
) -> None:
    weaviate_mock.expect_request("/v1/schema/Test").respond_with_json(
        response_json={"error": [{"message": "this is an error"}]}, status=403
    )

    client = weaviate.connect_to_local(
        port=MOCK_PORT, host=MOCK_IP, grpc_port=MOCK_PORT_GRPC, skip_init_checks=True
    )
    collection = client.collections.use("Test")

    with pytest.raises(InsufficientPermissionsError) as e1:
        collection.config.get()
    assert "this is an error" in e1.value.message

    with pytest.raises(UnexpectedStatusCodeError) as e2:
        collection.config.get()
    assert e2.value.status_code == 403

    weaviate_mock.check_assertions()


def test_old_version(ready_mock: HTTPServer, start_grpc_server: grpc.Server) -> None:
    ready_mock.expect_request("/v1/meta").respond_with_json({"version": "1.23.4"})
    with pytest.raises(WeaviateStartUpError):
        weaviate.connect_to_local(port=MOCK_PORT, host=MOCK_IP, skip_init_checks=True)
    ready_mock.check_assertions()


def test_closed_connection(weaviate_auth_mock: HTTPServer, start_grpc_server: grpc.Server) -> None:
    client = weaviate.WeaviateClient(
        ConnectionParams(
            grpc=ProtocolParams(host=MOCK_IP, port=MOCK_PORT_GRPC, secure=False),
            http=ProtocolParams(host=MOCK_IP, port=MOCK_PORT, secure=False),
        )
    )
    with pytest.raises(weaviate.exceptions.WeaviateClosedClientError):
        client.collections.list_all()
    with pytest.raises(weaviate.exceptions.WeaviateClosedClientError):
        collection = client.collections.use("Test")
        collection.query.fetch_objects()
    with pytest.raises(weaviate.exceptions.WeaviateClosedClientError):
        collection = client.collections.use("Test")
        collection.data.insert_many([{}])


def test_missing_multi_tenancy_config(
    weaviate_mock: HTTPServer, start_grpc_server: grpc.Server
) -> None:
    vic = VectorIndexConfigFlat(
        quantizer=None,
        distance_metric=VectorDistances.COSINE,
        vector_cache_max_objects=10,
        multi_vector=None,
    )
    vic.distance = vic.distance_metric  # type: ignore
    response_json = CollectionConfig(
        name="Test",
        description="",
        generative_config=None,
        reranker_config=None,
        vectorizer_config=None,
        vector_config=None,
        inverted_index_config=InvertedIndexConfig(
            bm25=BM25Config(b=0, k1=0),
            cleanup_interval_seconds=0,
            index_null_state=False,
            index_property_length=False,
            index_timestamps=False,
            stopwords=StopwordsConfig(preset=StopwordsPreset.NONE, additions=[], removals=[]),
        ),
        multi_tenancy_config=MultiTenancyConfig(
            enabled=True, auto_tenant_creation=False, auto_tenant_activation=False
        ),
        sharding_config=ShardingConfig(
            virtual_per_physical=0,
            desired_count=0,
            actual_count=0,
            desired_virtual_count=0,
            actual_virtual_count=0,
            key="",
            strategy="",
            function="",
        ),
        properties=[],
        references=[],
        replication_config=ReplicationConfig(
            factor=0,
            async_enabled=False,
            deletion_strategy=ReplicationDeletionStrategy.NO_AUTOMATED_RESOLUTION,
        ),
        vector_index_config=vic,
        vector_index_type=VectorIndexType.FLAT,
        vectorizer=Vectorizers.NONE,
    ).to_dict()

    weaviate_mock.expect_request("/v1/schema/TestTrue").respond_with_json(
        response_json=response_json, status=200
    )
    client = weaviate.connect_to_local(
        port=MOCK_PORT, host=MOCK_IP, grpc_port=MOCK_PORT_GRPC, skip_init_checks=True
    )
    collection = client.collections.use("TestTrue")
    conf = collection.config.get()
    assert conf.multi_tenancy_config.enabled is True

    # Delete the missing configuration for multy tenancy
    response_json["name"] = "TestFalse"
    del response_json["multiTenancyConfig"]
    weaviate_mock.expect_request("/v1/schema/TestFalse").respond_with_json(
        response_json=response_json, status=200
    )
    client = weaviate.connect_to_local(
        port=MOCK_PORT, host=MOCK_IP, grpc_port=MOCK_PORT_GRPC, skip_init_checks=True
    )
    collection = client.collections.use("TestFalse")

    conf = collection.config.get()
    assert conf.multi_tenancy_config.enabled is False


def test_return_from_bind_module(
    weaviate_auth_mock: HTTPServer, start_grpc_server: grpc.Server
) -> None:
    config = wvc.config.Configure

    # point of this test is to check if the return from the bind module is correctly parsed. There is no skip and vectorizePropertyName present
    prop_modconf: Dict[str, Any] = {"multi2vec-bind": {}}

    hnsw_config = config.VectorIndex.hnsw(
        1, VectorDistances.COSINE, 1, 1, 1, 1, 1, None, 1, 1, 1
    )._to_dict()
    hnsw_config["skip"] = True
    ii_config = config.inverted_index(
        1, 1, 1, True, True, True, StopwordsPreset.EN, [], []
    )._to_dict()
    schema = {
        "class": "TestBindCollection",
        "properties": [
            {
                "dataType": ["text"],
                "name": "name",
                "indexFilterable": False,
                "indexSearchable": False,
                "moduleConfig": prop_modconf,
            },
        ],
        "vectorIndexConfig": hnsw_config,
        "vectorIndexType": "hnsw",
        "invertedIndexConfig": ii_config,
        "multiTenancyConfig": config.multi_tenancy()._to_dict(),
        "vectorizer": "multi2vec-bind",
        "replicationConfig": {"factor": 2, "asyncEnabled": False},
        "moduleConfig": {"multi2vec-bind": {}},
    }
    weaviate_auth_mock.expect_request("/v1/schema/TestBindCollection").respond_with_json(
        response_json=schema, status=200
    )
    client = weaviate.connect_to_local(
        port=MOCK_PORT, host=MOCK_IP, grpc_port=MOCK_PORT_GRPC, skip_init_checks=True
    )
    collection = client.collections.use("TestBindCollection")
    conf = collection.config.get()

    assert conf.properties[0].vectorizer_config is not None
    assert not conf.properties[0].vectorizer_config.skip
    assert not conf.properties[0].vectorizer_config.vectorize_property_name


@pytest.mark.parametrize(
    "integrations,headers",
    [
        (wvc.config.Integrations.cohere(api_key="key"), {"X-Cohere-Api-Key": "key"}),
        (
            wvc.config.Integrations.cohere(
                api_key="key", requests_per_minute_embeddings=50, base_url="http://some-url.com"
            ),
            {
                "X-Cohere-Api-Key": "key",
                "X-Cohere-Ratelimit-RequestPM-Embedding": "50",
                "X-Cohere-Baseurl": "http://some-url.com",
            },
        ),
        ([wvc.config.Integrations.cohere(api_key="key")], {"X-Cohere-Api-Key": "key"}),
        (
            [
                wvc.config.Integrations.cohere(api_key="key"),
                wvc.config.Integrations.openai(api_key="key2"),
            ],
            {"X-Cohere-Api-Key": "key", "X-Openai-Api-Key": "key2"},
        ),
        (
            [
                wvc.config.Integrations.voyageai(
                    api_key="key", base_url="http://some-url.com", requests_per_minute_embeddings=50
                )
            ],
            {
                "X-Voyageai-Api-Key": "key",
                "X-Voyageai-Ratelimit-RequestPM-Embedding": "50",
                "X-Voyageai-Baseurl": "http://some-url.com",
            },
        ),
        (
            [
                wvc.config.Integrations.jinaai(
                    api_key="key", base_url="http://some-url.com", requests_per_minute_embeddings=50
                )
            ],
            {
                "X-Jinaai-Api-Key": "key",
                "X-Jinaai-Ratelimit-RequestPM-Embedding": "50",
                "X-Jinaai-Baseurl": "http://some-url.com",
            },
        ),
    ],
)
def test_integration_config(
    weaviate_no_auth_mock: HTTPServer,
    start_grpc_server: grpc.Server,
    integrations: _IntegrationConfig,
    headers: Dict[str, Any],
) -> None:
    client = weaviate.connect_to_local(
        port=MOCK_PORT,
        host=MOCK_IP,
        grpc_port=MOCK_PORT_GRPC,
    )

    client.integrations.configure(integrations)

    weaviate_no_auth_mock.expect_request("/v1/schema", headers=headers).respond_with_json(
        status=200, response_json={"classes": []}
    )

    client.collections.list_all()  # return is irrelevant
    weaviate_no_auth_mock.check_assertions()


def test_year_zero(year_zero_collection: weaviate.collections.Collection) -> None:
    with pytest.warns(UserWarning) as recwarn:
        objs = year_zero_collection.query.fetch_objects().objects
        assert objs[0].properties["date"] == datetime.datetime.min

        assert str(recwarn[0].message).startswith("Con004")


@pytest.mark.parametrize("output", ["minimal", "verbose"])
def test_node_with_timeout(
    httpserver: HTTPServer, start_grpc_server: grpc.Server, output: Literal["minimal", "verbose"]
) -> None:
    httpserver.expect_request("/v1/.well-known/ready").respond_with_json({})
    httpserver.expect_request("/v1/meta").respond_with_json({"version": "1.24"})

    httpserver.expect_request("/v1/nodes").respond_with_json(
        status=200,
        response_json={"nodes": [{"status": "TIMEOUT", "shards": None, "name": "node1"}]},
    )

    client = weaviate.connect_to_local(
        port=MOCK_PORT,
        host=MOCK_IP,
        grpc_port=MOCK_PORT_GRPC,
    )

    nodes = client.cluster.nodes(output=output)
    assert nodes[0].status == "TIMEOUT"


def test_backup_cancel_while_create_and_restore(
    weaviate_no_auth_mock: HTTPServer, start_grpc_server: grpc.Server
) -> None:
    client = weaviate.connect_to_local(
        port=MOCK_PORT,
        host=MOCK_IP,
        grpc_port=MOCK_PORT_GRPC,
    )

    backup_id = "id"

    weaviate_no_auth_mock.expect_request("/v1/backups/filesystem").respond_with_json(
        {
            "collections": ["backupTest"],
            "status": "STARTED",
            "path": "path",
            "id": backup_id,
        }
    )
    weaviate_no_auth_mock.expect_request("/v1/backups/filesystem/" + backup_id).respond_with_json(
        {
            "collections": ["backupTest"],
            "status": "CANCELED",
            "path": "path",
            "id": backup_id,
        }
    )

    weaviate_no_auth_mock.expect_request(
        "/v1/backups/filesystem/" + backup_id + "/restore"
    ).respond_with_json(
        {
            "collections": ["backupTest"],
            "status": "CANCELED",
            "path": "path",
            "id": backup_id,
        }
    )

    with pytest.raises(BackupCanceledError):
        client.backup.create(
            backup_id=backup_id,
            backend=BackupStorage.FILESYSTEM,
            wait_for_completion=True,
        )

    with pytest.raises(BackupCanceledError):
        client.backup.restore(
            backup_id=backup_id,
            backend=BackupStorage.FILESYSTEM,
            wait_for_completion=True,
        )


def test_grpc_retry_logic(
    retries: tuple[weaviate.collections.Collection, MockRetriesWeaviateService],
) -> None:
    collection = retries[0]
    service = retries[1]

    with pytest.raises(weaviate.exceptions.WeaviateQueryError):
        # checks first call correctly handles INTERNAL error
        collection.query.fetch_objects()

    # should perform one retry and then succeed subsequently
    objs = collection.query.fetch_objects().objects
    assert len(objs) == 1
    assert objs[0].properties["name"] == "test"
    assert service.search_count == 2

    with pytest.raises(weaviate.exceptions.WeaviateTenantGetError):
        # checks first call correctly handles error that isn't UNAVAILABLE
        collection.tenants.get()

    # should perform one retry and then succeed subsequently
    tenants = list(collection.tenants.get().values())
    assert len(tenants) == 1
    assert tenants[0].name == "tenant1"
    assert service.tenants_count == 2


def test_grpc_forbidden_exception(forbidden: weaviate.collections.Collection) -> None:
    with pytest.raises(weaviate.exceptions.InsufficientPermissionsError):
        forbidden.query.fetch_objects()

    with pytest.raises(weaviate.exceptions.InsufficientPermissionsError):
        forbidden.tenants.get()

    with pytest.raises(weaviate.exceptions.InsufficientPermissionsError):
        forbidden.data.delete_many(where=wvc.query.Filter.by_property("name").equal("test"))

    with pytest.raises(weaviate.exceptions.InsufficientPermissionsError):
        forbidden.data.insert_many([{"name": "test"}])
