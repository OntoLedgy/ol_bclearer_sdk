UNWIND $batch as row
MATCH (a {node_id: row.start_node}), (b {node_id: row.end_node})
MERGE (a)-[r:relationship]->(b);
