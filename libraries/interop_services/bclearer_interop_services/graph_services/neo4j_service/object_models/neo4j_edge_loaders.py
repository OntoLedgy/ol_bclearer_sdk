import pandas as pd
import concurrent.futures
class EdgeLoader:
    def __init__(self, neo4j_wrapper):
        self.neo4j_wrapper = neo4j_wrapper

    def load_edges(self, csv_file, edge_label, mapping_query):
        df = pd.read_csv(csv_file)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._load_edge, row.to_dict(), edge_label, mapping_query)
                for _, row in df.iterrows()
            ]
            concurrent.futures.wait(futures)

    def _load_edge(self, row, edge_label, mapping_query):
        query = mapping_query.format(**row)
        self.neo4j_wrapper.run_query(query)
