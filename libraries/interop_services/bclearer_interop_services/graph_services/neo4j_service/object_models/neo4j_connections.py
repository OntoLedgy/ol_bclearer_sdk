from neo4j import GraphDatabase

from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_sessions import (
    Neo4jSession,
)


class Neo4jConnections:
    def __init__(
        self,
        uri=None,
        database_name=None,
        user_name=None,
        password=None,
        max_connection_pool_size=None,
        external_driver=None,  # New parameter to accept an existing driver
    ):

        self.uri = uri
        self.auth = (
            user_name,
            password,
        )
        self.database_name = (
            database_name
        )
        self.external_driver = (
            external_driver
        )

        # Use the external driver if provided, otherwise create a new one
        if self.external_driver:
            self.driver = (
                self.external_driver
            )
        else:
            self.driver = self.get_driver(
                max_connection_pool_size,
            )

    def get_driver(
        self,
        max_connection_pool_size=None,
    ):
        # Only get a new driver if one is not passed externally
        if not self.external_driver:
            self.driver = GraphDatabase.driver(
                uri=self.uri,
                auth=self.auth,
                max_connection_pool_size=max_connection_pool_size,
            )
        return self.driver

    def get_new_session(
        self, database_name=None,
    ):
        # Use the driver (whether external or created internally)
        if database_name:
            session = Neo4jSession(
                driver=self.driver,
                database_name=database_name,
            )
        else:
            session = Neo4jSession(
                driver=self.driver,
                database_name=self.database_name,
            )
        return session

    def close(self):
        # Only close the driver if it's not an external one
        if not self.external_driver:
            self.driver.close()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        self.close()
