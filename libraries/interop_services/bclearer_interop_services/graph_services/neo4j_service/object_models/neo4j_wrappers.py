# from neo4j_object_models.neo4j_connections import Neo4jConnection

from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_connections import (
    Neo4jConnections,
)


class Neo4jWrapper:
    def __init__(
        self,
        neo4jconnection: Neo4jConnections,
    ):
        self.driver = (
            neo4jconnection.driver
        )
        self.neo4jconnection = (
            neo4jconnection
        )

    def close(self):
        self.driver.close()

    def run_query(
        self,
        query,
        parameters=None,
    ):
        with self.driver.session(
            database=self.neo4jconnection.database_name,
        ) as session:
            result = session.run(
                query,
                parameters,
            )
            return result
