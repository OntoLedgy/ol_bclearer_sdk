from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_connections import (
    Neo4jConnections,
)
from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_databases import (
    Neo4jDatabases,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.helpers.prepare_dataset_dictionary_from_folder import (
    get_load_dataset,
    get_load_dataset_by_graph_object_type,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.helpers.read_cypher_queries import (
    generate_list_from_text,
)


class TestNeo4jStandardOperations:
    def test_delete_neo4j_database(
        self,
        neo4j_docker_database: Neo4jDatabases,
    ):
        self.cypher_query = (
            "MATCH (n) DETACH DELETE n"
        )

        session = neo4j_docker_database.get_new_session(
            neo4j_docker_database.connection.database_name,
        )

        session.execute_cypher_query(
            self.cypher_query,
        )

    def test_standard_query_execution(
        self,
        neo4j_docker_database: Neo4jDatabases,
    ):
        self.cypher_query = "CREATE INDEX index_name_for_cell_value FOR (cv:CellValue) ON (cv.uuid);"

        session = neo4j_docker_database.get_new_session(
            neo4j_docker_database.connection.database_name,
        )

        records = session.execute_cypher_query(
            self.cypher_query,
        )

        print(records)

    #
    # def test_query_list_execution(
    #     self,
    #     neo4j_connection,
    # ):
    #     self.cypher_queries = "CREATE INDEX index_name_for_column FOR (column:Column) ON (column.column_uuids);\
    #                             CREATE INDEX index_name_for_row FOR (row:Row) ON (row.row_uuids);\
    #                             CREATE INDEX index_name_for_cell_value FOR (cv:CellValue) ON (cv.uuid);\
    #                             CREATE INDEX index_name_for_cell_type FOR (celltype:CellType) ON (celltype.cell_type_uuids);\
    #                            CREATE INDEX index_name_for_physical_quantity FOR (physicalquantity:PhysicalQuantity) ON (physicalquantity.physical_quantity_uuids);\
    #                            CREATE INDEX index_name_for_standard_unit_of_measure FOR (standard_unit_of_measure:StandardUnitOfMeasure) ON (standard_unit_of_measure.standard_unit_of_measure_uuids);\
    #                            CREATE INDEX index_name_for_property_type FOR (property_type:PropertyType) ON (property_type.property_type_uuids);"
    #
    #     self.cypher_query_list = (
    #         generate_list_from_text(
    #             self.cypher_queries,
    #         )
    #     )
    #
    #     for (
    #         item
    #     ) in self.cypher_query_list:
    #         try:
    #             with neo4j_connection.get_new_session(
    #                 neo4j_connection.database_name,
    #             ) as session:
    #                 if len(item) > 0:
    #                     records = session.execute_cypher_query(
    #                         item,
    #                     )
    #
    #                 print(records)
    #         except:
    #             pass
    #
    # def test_load_dataset_generation(
    #     self,
    # ):
    #     data_input_folder_absolute_path = r"./data/graph"
    #
    #     load_dataset = get_load_dataset(
    #         data_input_folder_absolute_path,
    #     )
    #
    #     print(load_dataset)
    #
    #     print(load_dataset[10:])
    #
    # def test_load_dataset_by_category_generation(
    #     self,
    # ):
    #     data_input_folder_absolute_path = r"./data/graph"
    #
    #     load_dataset = get_load_dataset_by_graph_object_type(
    #         data_input_folder_absolute_path,
    #     )
    #
    #     print(load_dataset)
    #
    #     print(load_dataset[10:])
