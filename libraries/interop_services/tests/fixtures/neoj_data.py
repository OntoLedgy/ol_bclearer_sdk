import os

import pytest
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.helpers.read_cypher_queries import (
    read_cypher_query_from_file,
)


@pytest.fixture(scope="session")
def output_cypher_query_path(
    data_output_folder_absolute_path,
):
    query_relative_path = (
        "graph/output_query.cyp"
    )
    query_absolute_path = os.path.join(
        data_output_folder_absolute_path,
        query_relative_path,
    )
    return query_absolute_path


@pytest.fixture(scope="session")
def input_cypher_query_path(
    data_input_folder_absolute_path,
):
    query_relative_path = (
        "graph/query_list.cyp"
    )
    query_absolute_path = os.path.join(
        data_input_folder_absolute_path,
        query_relative_path,
    )
    return query_absolute_path


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
        "graph/synthetic_nodes.csv",
    )
    query_file_path_1 = os.path.join(
        data_input_folder_absolute_path,
        "graph/node_load.cyp",
    )
    query_1 = (
        read_cypher_query_from_file(
            query_file_path_1,
        )
    )

    csv_file_2 = os.path.join(
        data_input_folder_absolute_path,
        "graph/synthetic_nodes.csv",
    )
    query_file_path_2 = os.path.join(
        data_input_folder_absolute_path,
        "graph/node_load.cyp",
    )
    query_2 = (
        read_cypher_query_from_file(
            query_file_path_2,
        )
    )

    nodes_info = {
        "nodes_info": [
            {
                "csv_file": csv_file_1,
                "label": "object",
                "query": query_1,
            },
            {
                "csv_file": csv_file_2,
                "label": "object",
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
        "graph/synthetic_edges.csv",
    )
    query_file_path = os.path.join(
        data_input_folder_absolute_path,
        "graph/edge_load.cyp",
    )
    query = read_cypher_query_from_file(
        query_file_path,
    )

    edges_info = {
        "edges_info": [
            {
                "csv_file": csv_file,
                "label": "related",
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
