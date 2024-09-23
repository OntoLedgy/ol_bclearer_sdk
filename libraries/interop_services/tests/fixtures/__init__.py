import sys
import bclearer_interop_services.graph_services.neo4j_service as neo4j_service

sys.modules['neo4j_service'] = neo4j_service
