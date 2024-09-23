import pandas as pd
from neo4j_object_models import Neo4jConnection
#from bclearer_interop_services.code.services.graph_services.neo4j_service.object_models.Neo4jConnection import Neo4jConnection
from neo4j_object_models.Neo4jWrapper import Neo4jWrapper
from neo4j_orchestrators.NodeLoader import NodeLoader
from neo4j_orchestrators.EdgeLoader import EdgeLoader


class Neo4jDataLoadOrchestrator:
    def __init__(
            self, 
            neo4j_connection: Neo4jConnection,                        
            batch_size:int=1000):

        self.neo4j_wrapper = Neo4jWrapper(neo4j_connection)

        self.node_loader = NodeLoader(
            neo4j_wrapper=self.neo4j_wrapper,
            batch_size=batch_size
                        )
        self.edge_loader = EdgeLoader(
            neo4j_wrapper=self.neo4j_wrapper,
            batch_size=batch_size
            )
    
    def load_data(
            self, 
            nodes_info=None, 
            edges_info=None):
        

        
        if nodes_info:
            for node in nodes_info:
                node_dataframe = pd.read_csv(
                    node['csv_file'])
    
                node_dataframe.fillna(
                        value='', 
                        inplace=True)                  
                
                self.node_loader.load_nodes(
                    node_dataframe,                      
                    node['query'])
        
        if edges_info:
            
            for edge in edges_info:
                edge_dataframe = pd.read_csv(
                    edge['csv_file'])

                edge_dataframe.fillna(
                    value='', 
                    inplace=True)                  
        
                self.edge_loader.load_edges(
                    edge_dataframe,                      
                    edge['query'])

    def orchestrate_neo4j_data_load_from_csv(
            self,            
            object_info):

        # Determine the type of information provided (nodes, edges, or both)
        nodes_info = object_info.get('nodes_info')
        edges_info = object_info.get('edges_info')

        # Load the data
        self.load_data(
            nodes_info=nodes_info, 
            edges_info=edges_info
            )

        # Close the connection
        self.neo4j_wrapper.close()



        