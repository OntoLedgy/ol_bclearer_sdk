import os

from bclearer_interop_services.graph_services.neo4j_service.orchestrators.helpers.read_cypher_queries import (
    read_cypher_query_from_file,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.orchestrate_csv_to_neo4j_data_load import (
    orchestrate_csv_to_neo4j_load,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.prepare_dataset_dictionary_from_folder import (
    generate_load_dataset_from_folder,
)


def orchestrate_neo4j_load_dataset(
    root_folder,
    neo4j_connection,
):
    load_data_dictionary = generate_load_dataset_from_folder(
        root_folder,
    )

    load_dataset = iterate_structure(
        load_data_dictionary,
    )
    nodes_created = 0

    for pair in load_dataset:
        csv_path = pair["data"]
        cypher_path = pair["cypher"]
        csv_absolute_path = (
            os.path.join(
                root_folder,
                "load_files",
                csv_path,
            )
        )
        cypher_absolute_path = (
            os.path.join(
                root_folder,
                "queries",
                cypher_path,
            )
        )

        load_cypher_query = (
            read_cypher_query_from_file(
                cypher_absolute_path,
            )
        )

        print(
            f"Cypher Query:\n {load_cypher_query}\n",
        )

        nodes_created += orchestrate_csv_to_neo4j_load(
            csv_file_name_and_path=csv_absolute_path,
            neo4j_connection=neo4j_connection,
            cypher_load_query=load_cypher_query,
            batch_size=1000,
            concurrency=10,
            csv_file_encoding="UTF-8",
        )

    print(nodes_created)


def iterate_structure(structure):
    """This function takes a nested dictionary structure and returns a list of dictionaries,
    each containing the paths of the CSV and Cypher query pairs.

    Args:
    structure (dict): The input nested dictionary structure

    Returns:
    -------
    list: A list of dictionaries with 'data' and 'cypher' keys.

    """
    result = []

    def recurse(structure):
        for (
            key,
            value,
        ) in structure.items():
            if isinstance(value, dict):
                if (
                    "data" in value
                    and "cypher"
                    in value
                ):
                    csv_path = value[
                        "data"
                    ]
                    cypher_path = value[
                        "cypher"
                    ]
                    result.append(
                        {
                            "data": csv_path,
                            "cypher": cypher_path,
                        },
                    )
                else:
                    recurse(value)

    recurse(structure)
    return result
