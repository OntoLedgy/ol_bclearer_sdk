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
