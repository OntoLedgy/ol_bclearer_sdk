import unittest
from unittest.mock import Mock, patch


class TestNeo4jLoader(
    unittest.TestCase,
):
    def setUp(self):
        self.mock_session = Mock()
        self.mock_connection = Mock(
            return_value=self.mock_session,
        )

        patcher = patch(
            "source.code.neo4j_services.object_models.neo4j_connections",
            self.mock_connection,
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        self.test_data = [
            {"name": "Node1"},
            {"name": "Node2"},
        ]
        print("connecting")

        self.config_file = r"C:\Apps\S\bclearer_common_services\graph_processing_services\source\sandpit\MKh\config.ini"
        self.cypher_query = "UNWIND $batch AS row CREATE (n:TestNode {name: row.name})"

        self.batchSize = 2
        self.debug = False
        self.maxQueueSize = 10000

        self.loader = Neo4jLoader(
            threadID=1,
            name="TestLoader",
            config_file=self.config_file,
            cypher_query=self.cypher_query,
            batchSize=self.batchSize,
            out=Mock(),
            debug=self.debug,
            maxQueueSize=self.maxQueueSize,
        )

    def test_add_row_and_run(self):
        for row in self.test_data:
            self.loader.addRow(row)

        self.loader.run()
        self.loader.finish()

        self.assertEqual(
            len(self.loader.rows),
            0,
        )

    def test_finish(self):
        self.loader.finish()
        self.assertFalse(
            self.loader.ListenQueue,
        )

    # Add more test cases as needed to cover different scenarios


if __name__ == "__main__":
    print("starting test")
    unittest.main()
