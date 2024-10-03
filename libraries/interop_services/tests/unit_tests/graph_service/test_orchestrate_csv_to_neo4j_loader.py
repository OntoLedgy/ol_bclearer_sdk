from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_databases import (
    Neo4jDatabases,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.neo4j_data_load_orchestrators import (
    Neo4jDataLoadOrchestrators,
)


class TestNeo4jCsvLoad:

    def test_neo4j_to_csv_load_orchestation(
        self,
        nodes_info,
        edges_info,
        neo4j_docker_database,
    ):

        orchestrator = (
            Neo4jDataLoadOrchestrators(
                neo4j_docker_database
            )
        )

        # Load the data
        orchestrator.load_data(
            nodes_info,
            edges_info,
        )

        # Query to check if nodes were loaded
        query_nodes = """
        MATCH (n)
        RETURN n.node_id AS node_id, labels(n)[0] AS label, n.name AS name
        """

        result_nodes = neo4j_docker_database.run_query(
            query_nodes
        )

        # Print or assert the loaded nodes
        print(
            "Loaded Nodes:",
            result_nodes,
        )
        assert (
            len(result_nodes) > 0
        ), "No nodes were loaded into the database."

        # Query to check if edges were loaded (relationships)
        query_edges = """
        MATCH (n1)-[r]->(n2)
        RETURN n1.node_id AS start_node, n2.node_id AS end_node, type(r) AS relationship
        """

        result_edges = neo4j_docker_database.run_query(
            query_edges
        )

        # Print or assert the loaded edges
        print(
            "Loaded Edges:",
            result_edges,
        )
        assert (
            len(result_edges) > 0
        ), "No edges were loaded into the database."

        neo4j_docker_database.close()
