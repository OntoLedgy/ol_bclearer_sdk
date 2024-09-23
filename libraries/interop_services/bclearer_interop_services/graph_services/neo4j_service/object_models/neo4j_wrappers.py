from neo4j_object_models.Neo4jConnection import Neo4jConnection

class Neo4jWrapper:
    def __init__(
            self, 
            neo4jconnection:Neo4jConnection):
        
        self.driver = neo4jconnection.driver
        self.neo4jconnection = neo4jconnection        
    
    def close(self):
        self.driver.close()
    
    def run_query(
            self, 
            query, 
            parameters=None):
        
        with self.driver.session(database=self.neo4jconnection.database_name) as session:
            result = session.run(query, parameters)
            return result
