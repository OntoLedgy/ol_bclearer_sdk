from neo4j import Driver, GraphDatabase


class Neo4jWrapper:
    def __init__(
        self,
        uri=None,
        user=None,
        password=None,
        external_driver: Driver = None,
    ):
        if external_driver is None:
            self.driver = GraphDatabase.driver(
                uri,
                auth=(
                    user,
                    password,
                ),
            )
        else:
            self.driver = external_driver

    def close(self):
        self.driver.close()

    def run_query(
        self,
        query,
        parameters=None,
    ):
        with self.driver.session() as session:
            result = session.run(
                query,
                parameters,
            )
            return result
