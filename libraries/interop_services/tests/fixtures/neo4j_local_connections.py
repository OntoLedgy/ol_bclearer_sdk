from bclearer_interop_services.graph_services.neo4j_service.configurations.neo4j_configurations import (
    Neo4jConfigurations,
)
from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_connections import (
    Neo4jConnections,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.helpers.read_cypher_queries import (
    read_cypher_query_from_file,
)
from tests.fixtures.paths import *


@pytest.fixture(scope="session")
def neo4j_connection(
    configurations_folder,
):
    neo4j_configuration_file_name = (
        "neo4j_configuration.json"
    )

    neo4j_configuration_file = os.path.normpath(
        os.path.join(
            configurations_folder,
            neo4j_configuration_file_name,
        ),
    )

    neo4j_configuration = (
        Neo4jConfigurations(
            neo4j_configuration_file,
        )
    )

    neo4j_connection = Neo4jConnections(
        uri=neo4j_configuration.uri,
        database_name=neo4j_configuration.database_name,
        user_name=neo4j_configuration.username,
        password=neo4j_configuration.password,
    )

    return neo4j_connection


@pytest.fixture(scope="session")
def neo4j_loader_configuration_path(
    configurations_folder,
):
    neo4j_loader_configuration_file_name = (
        "csv_loader_configuration.json"
    )
    neo4j_loader_configuration_file_absolute_path = os.path.normpath(
        os.path.join(
            configurations_folder,
            neo4j_loader_configuration_file_name,
        ),
    )
    return neo4j_loader_configuration_file_absolute_path
