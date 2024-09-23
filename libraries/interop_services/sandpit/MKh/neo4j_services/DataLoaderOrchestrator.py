from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_node_loaders import NodeLoader
from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_edge_loaders import EdgeLoader
class DataLoaderOrchestrator:
    def __init__(self, neo4j_wrapper):
        self.neo4j_wrapper = neo4j_wrapper
        self.node_loader = NodeLoader(neo4j_wrapper)
        self.edge_loader = EdgeLoader(neo4j_wrapper)

    def load_data(self, nodes_info, edges_info):
        for node in nodes_info:
            self.node_loader.load_nodes(node['csv_file'], node['label'], node['query'])

        for edge in edges_info:
            self.edge_loader.load_edges(edge['csv_file'], edge['label'], edge['query'])
