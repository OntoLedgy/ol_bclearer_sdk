class TestNeo4jDocker:
    def test_neo4j_connection(
        self,
        neo4j_docker_driver,
    ):
        with neo4j_docker_driver.session() as session:
            result = session.run(
                "RETURN 1 AS number",
            )
            record = result.single()
            assert record["number"] == 1

    def test_neo4j_deploy_and_keep_open(
        self,
        start_neo4j_container,
    ):
        # You can now interact with the running Neo4j instance
        print(
            "Neo4j container is up and running for further interaction.",
        )

        # Test to shutdown Neo4j container on demand

    def test_neo4j_shutdown(
        self,
        neo4j_shutdown_container,
    ):
        print(
            "Shutting down Neo4j container.",
        )

    def test_with_custom_connection(
        self,
        neo4j_docker_connection,
    ):
        session = neo4j_docker_connection.get_new_session()

        result = session.execute_cypher_query(
            "RETURN 1 AS number",
        )
        record = result[0]
        assert record["number"] == 1

        neo4j_docker_connection.close()  # No driver will be closed if passed externally
