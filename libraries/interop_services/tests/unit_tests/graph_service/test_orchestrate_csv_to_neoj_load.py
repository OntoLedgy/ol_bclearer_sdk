import pytest
#from bclearer_interop_services.code.services.graph_services.neo4j_service.orchestrators.DataLoadOrchestrator import Neo4jDataLoadOrchestrator
from orchestrators.DataLoadOrchestrator import Neo4jDataLoadOrchestrator

from orchestrators.orchestrate_csv_folders_to_neo4j_load import orchestrate_csv_folders_to_neo4j_load

class TestNeo4jInteropServices(
            ):
    @pytest.fixture(autouse=True)        
    def setup_method(self):
        self.neo4j_data_orchestrator = Neo4jDataLoadOrchestrator        
        

    def test_single_file_loading(
                self,
                neo4j_connection,
                node_info
                ):
        single_node_info = node_info["nodes_info"][0]
        
        self.neo4j_data_orchestrator.orchestrate_neo4j_data_load_from_csv(
            neo4j_connection=neo4j_connection,
            object_info=single_node_info)         
      

    def test_multi_file_loading(
                self,
                neo4j_connection,
                object_info):
        
        self.neo4j_data_orchestrator.orchestrate_neo4j_data_load_from_csv(
            neo4j_connection=neo4j_connection,
            object_info=object_info)


    def test_multi_file_loading_from_folder(
            self,
            neo4j_connection,
            neo4j_loader_configuration_path            ):
        
        orchestrate_csv_folders_to_neo4j_load(
                neo4j_loader_configuration_path=neo4j_loader_configuration_path,          
			    neo4j_connection=neo4j_connection
		)        

          