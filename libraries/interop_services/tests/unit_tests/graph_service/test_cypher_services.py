import pytest
from bclearer_interop_services.graph_services.neo4j_service.object_models.cypher_queries import (
    CypherQueryWrapper,
)


class TestCypherServices:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.cypher_wrapper = (
            CypherQueryWrapper()
        )

    # Example usage:
    def test_cypher_wrapper_read_write(
        self,
        output_cypher_query_path,
        input_cypher_query_path,
    ):
        # Read query from a file
        self.cypher_wrapper.read_from_file(
            input_cypher_query_path,
        )

        # Validate the query
        self.cypher_wrapper.validate()

        # Write query to a file
        self.cypher_wrapper.write_to_file(
            output_cypher_query_path,
        )

    def test_cypher_wrapper_generate(
        self,
    ):
        find_nodes_query = CypherQueryWrapper.generate_find_all_nodes(
            "Person",
        )

        find_edges_query = CypherQueryWrapper.generate_find_all_edges(
            "FRIEND",
        )

        create_node_query = CypherQueryWrapper.generate_create_node(
            "Person",
            {
                "name": "Alice",
                "age": 30,
            },
        )

        print(find_nodes_query)
        print(find_edges_query)
        print(create_node_query)
