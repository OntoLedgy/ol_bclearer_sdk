import pytest
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.neo4j_data_load_orchestrators import (
    Neo4jDataLoadOrchestrators,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.orchestrate_csv_folders_to_neo4j_load import (
    orchestrate_csv_folders_to_neo4j_load,
)


class TestNeo4jInteropServices:

    @pytest.fixture(autouse=True)
    def setup_method(
        self, neo4j_docker_database
    ):
        self.neo4j_data_orchestrator = (
            Neo4jDataLoadOrchestrators(
                neo4j_docker_database
            )
        )

    def test_single_file_loading(
        self,
        node_info,
    ):
        single_node_info = node_info[
            "data"
        ][0]

        self.neo4j_data_orchestrator.orchestrate_neo4j_data_load_from_csv(
            object_info=single_node_info,
        )

    #
    # def test_multi_file_loading(
    #         self,
    #         object_info,
    #         ):
    #     self.neo4j_data_orchestrator.orchestrate_neo4j_data_load_from_csv(
    #
    #             object_info=object_info,
    #             )
    #
    #
    # def test_multi_file_loading_from_folder(
    #         self,
    #         neo4j_loader_configuration_path,
    #         ):
    #     orchestrate_csv_folders_to_neo4j_load(
    #             neo4j_loader_configuration_path=neo4j_loader_configuration_path,
    #             )
