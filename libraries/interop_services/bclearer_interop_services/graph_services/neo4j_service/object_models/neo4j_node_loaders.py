import pandas as pd


class NodeLoader:
    def __init__(self, neo4j_wrapper):
        self.neo4j_wrapper = neo4j_wrapper

    def load_nodes(self, csv_file, node_label, mapping_query):
        df = pd.read_csv(csv_file)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._load_node, row.to_dict(), node_label, mapping_query)
                for _, row in df.iterrows()
            ]
            concurrent.futures.wait(futures)

    def _load_node(self, row, node_label, mapping_query):
        query = mapping_query.format(**row)
        self.neo4j_wrapper.run_query(query)
