import concurrent
import logging
import time
from concurrent.futures import (
    ThreadPoolExecutor,
)

from neo4j_object_models.Neo4jWrapper import (
    Neo4jWrapper,
)

logging.basicConfig(level=logging.DEBUG)


class NodeLoader:
    def __init__(
        self,
        neo4j_wrapper: Neo4jWrapper,
        batch_size=1000,
        max_retries=3,
        retry_delay=1,
    ):

        self.neo4j_wrapper = (
            neo4j_wrapper
        )
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.retru_delay = retry_delay

    def load_nodes(
        self,
        node_data,
        mapping_query,
    ):

        with ThreadPoolExecutor() as executor:

            futures = [
                executor.submit(
                    self._load_node_batch,
                    node_data[
                        i : i
                        + self.batch_size
                    ],
                    mapping_query,
                )
                for i in range(
                    0,
                    len(node_data),
                    self.batch_size,
                )
            ]

            concurrent.futures.wait(
                futures,
            )

    def _load_node_batch(
        self, batch_df, mapping_query,
    ):

        for attempt in range(
            self.max_retries,
        ):
            try:

                batch = (
                    batch_df.to_dict(
                        orient="records",
                    )
                )

                logging.debug(
                    f"Executing batch query with {len(batch)} rows.",
                )

                self.neo4j_wrapper.run_query(
                    mapping_query,
                    parameters={
                        "batch": batch,
                    },
                )

            except Exception as e:
                logging.exception(
                    f"Error executing query: {e} \n Query: {mapping_query} \n Data: \n {batch}",
                )

                if (
                    "DeadlockDetected"
                    in str(e)
                ):
                    if (
                        attempt
                        < self.max_retries
                        - 1
                    ):

                        logging.warning(
                            f"Deadlock detected. Retrying in {self.retry_delay} seconds...",
                        )

                        time.sleep(
                            self.retry_delay,
                        )

                    else:
                        logging.exception(
                            "Max retries reached. Failing batch.",
                        )
                        raise
                else:
                    raise

    def load_node(self, node_info):
        pass
