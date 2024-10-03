UNWIND $batch as row
MERGE (n {node_id: toInteger(row.node_id)})
SET n.label = row.label, n.name = row.name;
