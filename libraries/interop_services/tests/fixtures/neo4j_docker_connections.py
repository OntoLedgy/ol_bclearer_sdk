import time

import docker
import pytest
from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_databases import (
    Neo4jDatabases,
)


@pytest.fixture(scope="session")
def neo4j_container():
    docker_client = docker.from_env()
    neo4j_container = docker_client.containers.run(
        "neo4j:latest",
        name="test_neo4j",
        environment={
            "NEO4J_AUTH": "neo4j/testpassword",
        },
        ports={
            "7687/tcp": 7687,
            "7474/tcp": 7474,
        },
        detach=True,
    )
    # Wait for the neo4j_container to fully start and Neo4j to be ready
    time.sleep(
        15,
    )  # Increase the wait time if needed
    logs = neo4j_container.logs()
    print(
        logs.decode("utf-8"),
    )  # Print logs to ensure the neo4j_container is running

    yield neo4j_container

    neo4j_container.stop()
    neo4j_container.remove()


@pytest.fixture(scope="session")
def neo4j_docker_driver(
    neo4j_container,
):
    from neo4j import GraphDatabase

    uri = "bolt://localhost:7687"

    neo4j_docker_driver = (
        GraphDatabase.driver(
            uri,
            auth=(
                "neo4j",
                "testpassword",
            ),
        )
    )

    yield neo4j_docker_driver

    neo4j_docker_driver.close()


@pytest.fixture(scope="session")
def neo4j_docker_connection(
    neo4j_container,
):
    from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_connections import (
        Neo4jConnections,
    )

    uri = "bolt://localhost:7687"
    auth = ("neo4j", "testpassword")

    neo4j_connection = Neo4jConnections(
        uri=uri,
        user_name=auth[0],
        password=auth[1],
    )

    yield neo4j_connection

    neo4j_connection.close()


@pytest.fixture(scope="session")
def neo4j_docker_database(
    neo4j_docker_connection,
):
    from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_databases import (
        Neo4jDatabases,
    )

    neo4j_wrapper = Neo4jDatabases(
        external_connection=neo4j_docker_connection
    )

    yield neo4j_wrapper

    neo4j_wrapper.close()


# @pytest.fixture(scope="session")
# def start_neo4j_container():
#     client = docker.from_env()
#     container = client.containers.run(
#         "neo4j:latest",
#         name="open_neo4j",
#         environment={
#             "NEO4J_AUTH": "neo4j/testpassword",
#         },
#         ports={
#             "7687/tcp": 7687,
#             "7474/tcp": 7474,
#         },
#         detach=True,
#     )
#     # Wait for Neo4j to initialize
#     time.sleep(15)
#     logs = container.logs()
#     print(
#         "Neo4j container logs:",
#         logs.decode("utf-8"),
#     )
#
#     # Yield the container for interaction
#     yield container
#
#     # Do not stop or remove the container to leave it running
#     print(
#         "Neo4j container is still running for interaction.",
#     )

#
# @pytest.fixture(scope="session")
# def neo4j_shutdown_container():
#     client = docker.from_env()
#
#     container = client.containers.get(
#         "open_neo4j",
#     )
#
#     # Yield the container for shutdown action
#     yield container
#
#     # Stop and remove the container
#     container.stop()
#     container.remove()
#     print(
#         "Neo4j container has been shut down and removed.",
#     )
