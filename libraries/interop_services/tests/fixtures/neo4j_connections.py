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


@pytest.fixture(scope="session")
def node_info():

    test_data = [
        {"name": "Node1"},
        {"name": "Node2"},
    ]

    cypher_query = "UNWIND $batch AS row CREATE (n:Node {name: row.name})"

    node_info = {
        "data": test_data,
        "query": cypher_query,
    }
    return node_info


@pytest.fixture(scope="session")
def nodes_info(
    data_input_folder_absolute_path,
):
    csv_file_1 = os.path.join(
        data_input_folder_absolute_path,
        "graph\\cypher_data\\01_nodes\\r_01_neo4j_workbooks_nodes_all.csv",
    )
    query_file_path_1 = os.path.join(
        data_input_folder_absolute_path,
        "graph\\cypher_queries\\01_nodes\\r_01_neo4j_workbooks_nodes_all.cypher",
    )
    query_1 = (
        read_cypher_query_from_file(
            query_file_path_1,
        )
    )

    csv_file_2 = os.path.join(
        data_input_folder_absolute_path,
        "graph\\cypher_data\\01_nodes\\r_02_neo4j_sheets_nodes_all.csv",
    )
    query_file_path_2 = os.path.join(
        data_input_folder_absolute_path,
        "graph\\cypher_queries\\01_nodes\\r_02_neo4j_sheets_nodes_all.cypher",
    )
    query_2 = (
        read_cypher_query_from_file(
            query_file_path_1,
        )
    )

    nodes_info = {
        "nodes_info": [
            {
                "csv_file": csv_file_1,
                "label": "workbooks",
                "query": query_1,
            },
            {
                "csv_file": csv_file_2,
                "label": "sheets",
                "query": query_2,
            },
        ],
    }
    return nodes_info


@pytest.fixture(scope="session")
def edges_info(
    data_input_folder_absolute_path,
):

    csv_file = os.path.join(
        data_input_folder_absolute_path,
        "graph\\cypher_data\\02_edges\\r_01_neo4j_sheets_to_workbooks_edges_all.csv",
    )
    query_file_path = os.path.join(
        data_input_folder_absolute_path,
        "graph\\cypher_queries\\02_edges\\r_01_neo4j_sheets_to_workbooks_edges_all.cypher",
    )
    query = read_cypher_query_from_file(
        query_file_path,
    )

    edges_info = {
        "edges_info": [
            {
                "csv_file": csv_file,
                "label": "sheet_is_from_workbook",
                "query": query,
            },
        ],
    }
    return edges_info


@pytest.fixture(scope="session")
def graph_info(nodes_info, edges_info):

    graph_info = {
        "nodes_info": nodes_info,
        "edges_info": edges_info,
    }

    return graph_info
