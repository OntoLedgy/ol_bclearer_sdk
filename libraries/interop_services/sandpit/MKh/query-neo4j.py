import configparser

from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(
        self,
        uri,
        dbname,
        user,
        password,
    ):
        self._driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
        )
        self._dbname = dbname

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        self._driver.close()

    def run_query(self, query):
        with self._driver.session(
            database=self._dbname,
        ) as session:
            result = session.run(query)
            records = list(result)
            return records


def orchestrate_neo4j_cyper_query_execution():
    config = configparser.ConfigParser()
    config.read("config.ini")

    uri = config["neo4j"]["uri"]
    dbname = config["neo4j"]["dbname"]
    user = config["neo4j"]["user"]
    password = config["neo4j"]["password"]

    with Neo4jConnection(
        uri,
        dbname,
        user,
        password,
    ) as connection:
        while True:
            query = input(
                "Enter a Cypher query (or 'exit' to quit): ",
            )

            if query == "exit":
                break

            records = connection.run_query(
                query,
            )

            for record in records:
                print(record)


if __name__ == "__main__":
    orchestrate_neo4j_cyper_query_execution()
