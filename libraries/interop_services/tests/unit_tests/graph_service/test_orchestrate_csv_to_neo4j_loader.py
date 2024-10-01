from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_databases import Neo4jWrapper
from bclearer_interop_services.graph_services.neo4j_service.orchestrators import DataLoadOrchestrator


def test_neo4j_to_csv_load_orchestation(
        self,
        nodes_info,
        edges_info):

    # Instantiate the wrapper and orchestrator
    neo4j_wrapper = Neo4jWrapper('bolt://localhost:7687', 'neo4j', 'password')

    orchestrator = DataLoadOrchestrator(neo4j_wrapper)

    # Load the data
    orchestrator.load_data(nodes_info, edges_info)

    # Close the connection
    neo4j_wrapper.close()