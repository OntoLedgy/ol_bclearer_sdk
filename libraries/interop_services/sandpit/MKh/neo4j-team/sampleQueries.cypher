//Get Site info and one level below + issues at current Site
MATCH (r:Refinery)<-[:WHOLE_PART]-(s:Site {source_primary_key_hash: "0f718e9f7276015c61d702f118c308c7c34840f3080bfca333b7ef0c4f628a8a"})<-[:WHOLE_PART]-(p:Plant)
OPTIONAL match (s)-[:HAS_ISSUE]->(i:Issues)-[:HAS_ISSUE_TYPE]->(it:Issue_Type)
return r, s.name AS SiteName, s.description AS Description, s.source_system AS sourceSystem, count(distinct i) AS SiteIssues, count(distinct it) AS NbrOfSiteIssueTypes, count(p) as Plants

//RCC:
MATCH (r:Refinery)<-[wp0:WHOLE_PART]-(s:Site {source_primary_key_hash: "0f718e9f7276015c61d702f118c308c7c34840f3080bfca333b7ef0c4f628a8a"})<-[wp1:WHOLE_PART]-(p:Plant)
OPTIONAL match (s)-[hi:HAS_ISSUE]->(i:Issues)-[hit:HAS_ISSUE_TYPE]->(it:Issue_Type)
return s, p, i, hi, hit, it, wp0, wp1, s.name AS SiteName, s.description AS Description, s.source_system AS sourceSystem, count(distinct i) AS SiteIssues, count(distinct it) AS NbrOfSiteIssueTypes, count(p) as Plants

Started streaming 1 records after 111 ms and completed after 114 ms.

//Get Plant info and one level below + issues at current plant
MATCH (s:Site)<-[:WHOLE_PART]-(p:Plant {source_primary_key_hash: "b45650616452fc9c2f3e97f079f8fac99f693be448a7c4f0a8187ed8706fb065"})<-[:WHOLE_PART]-(pu:Process_Unit)
OPTIONAL match (p)-[:HAS_ISSUE]->(i:Issues)-[:HAS_ISSUE_TYPE]->(it:Issue_Type)
return s, p.name AS PlantName, p.description AS Description, p.source_system AS sourceSystem,count(distinct i) AS PlantIssues
, count(distinct it) AS NbrOfPlantIssueTypes ,count(pu) as PuCount order by PuCount desc 

Started streaming 1 records after 109 ms and completed after 111 ms.
//Get Pu info and one level below + issues at current PU
MATCH (s:Site)<-[:WHOLE_PART]-(:Plant)<-[:WHOLE_PART]-(pu:Process_Unit {source_primary_key_hash: "892a73ebe4f18da861808c9c325e737fc46372db09404bebc6a9f2e7a44e3698"})<-[:WHOLE_PART]-(t:Tag)
OPTIONAL match (pu)-[:HAS_ISSUE]->(i:Issues)-[:HAS_ISSUE_TYPE]->(it:Issue_Type)
return s, pu.name AS UnitName, pu.description AS Description, pu.source_system AS sourceSystem, count(distinct i) AS UnitIssues, count(distinct it) AS NbrOfUnitsIssueTypes,count(t) as TagCount order by TagCount desc 

Started streaming 1 records after 134 ms and completed after 136 ms.

//RCC
MATCH (s:Site)<-[wp0:WHOLE_PART]-(p:Plant)<-[wp1:WHOLE_PART]-(pu:Process_Unit)<-[wp2:WHOLE_PART]-(t:Tag)
OPTIONAL match (pu)-[hi:HAS_ISSUE]->(i:Issues)-[hit:HAS_ISSUE_TYPE]->(it:Issue_Type)
return s, p, pu, t, i, hi, hit, it, wp0, wp1, wp2, pu.name AS UnitName, pu.description AS Description, pu.source_system AS sourceSystem, count(distinct i) AS UnitIssues, count(distinct it) AS NbrOfUnitsIssueTypes,count(t) as TagCount 
order by TagCount desc 
limit 25

MATCH (s:Site)<-[wp0:WHOLE_PART]-(p:Plant)<-[wp1:WHOLE_PART]-(pu:Process_Unit)<-[wp2:WHOLE_PART]-(t:Tag)-[hi:HAS_ISSUE]->(i:Issues)-[hit:HAS_ISSUE_TYPE]->(it:Issue_Type)
return s, p, pu, t, i, hi, hit, it, wp0, wp1, wp2, pu.name AS UnitName, pu.description AS Description, pu.source_system AS sourceSystem, count(distinct i) AS UnitIssues, count(distinct it) AS NbrOfUnitsIssueTypes,count(t) as TagCount 
order by TagCount desc 
limit 25



//Get Tag info and one level below + issues at current Tag
MATCH (s:Site)<-[:WHOLE_PART]-(:Plant)<-[:WHOLE_PART]-(:Process_Unit)<-[:WHOLE_PART]-(t:Tag {source_primary_key_hash: "f62292f9be616d64769119a217589fdee039e39dcc969fe74788bf0e5d1d68f3"})
OPTIONAL match (t)-[:HAS_ISSUE]->(i:Issues)-[:HAS_ISSUE_TYPE]->(it:Issue_Type)
return s, t.name AS TagName, t.description AS Description, t.source_system AS sourceSystem, count(distinct i) AS TagIssues, count(distinct it) AS NbrOfTagIssueTypes

Started streaming 1 records after 134 ms and completed after 136 ms.

// Create fulltext search index on name and description for all entities(except issue & issuetype)
CREATE FULLTEXT INDEX nameAndDescriptions IF NOT EXISTS FOR (n:Entity|Refinery|Site|Plant|Process_Unit|Tag) ON EACH [n.name, n.description]

// search bar in tree view
CALL db.index.fulltext.queryNodes("nameAndDescriptions", "*"+$searchterm+"*") YIELD node, score
where score > 2
WITH node, [x in labels(node) where x <> "Entity"][0] as Type ,score limit 100
RETURN Type, node.name, node.description,score,node.source_system, reduce(a="", y in nodes([uppath=(node)-[:WHOLE_PART*]->(:Site)|uppath][0]) | a + ">" + [x in labels(y) where x <> "Entity"] [0] + " : " + y.name ) as upPath , count{(node)-[:HAS_ISSUE]->() } as issueCount

Started streaming 14 records after 103 ms and completed after 329 ms.

// create fulltext search index on name and description for issueType
CREATE FULLTEXT INDEX issueTypeDescription IF NOT EXISTS FOR (n:Issue_Type) ON EACH [n.name, n.description]

// the Issues view search
CALL db.index.fulltext.queryNodes("issueTypeDescription", "*"+$issueterm+"*") YIELD node, score
WITH node, score limit 100
MATCH (node)-[:HAS_ISSUE_TYPE]->(:Issues)<-[:HAS_ISSUE]-(e:Tag)
with node, score, e, [x in labels(e) where x <> "Entity"][0] as Type
//MATCH (i:Issues)<-[:HAS_ISSUE]-(e)<-[:WHOLE_PART*]-(children:Equipment)
MATCH (i:Issues)<-[:HAS_ISSUE]-(e)
RETURN Type, e.name, e.description,score,e.source_system, reduce(a="", y in nodes([uppath=(t)-[:WHOLE_PART*]->(:Site)|uppath][0]) | a + ">" + [x in labels(y) where x <> "Entity"][0] + " : " + y.name ) as upPath, i.name


Started streaming 2225 records after 102 ms and completed after 215 ms, displaying first 1000 rows.

// OR this query which is a bit slower but returns the lineage
CALL db.index.fulltext.queryNodes("issueTypeName", "*"+$issueterm+"*") YIELD node, score
WITH node, score limit 10
MATCH (node)<-[:HAS_ISSUE_TYPE]-(:Issues)<-[:HAS_ISSUE]-(e:Tag)
with node, score, e, [x in labels(e) where x <> "Entity"][0] as Type
MATCH (i:Issues)<-[:HAS_ISSUE]-(e)
with node, e, i, Type, score
CALL apoc.path.subgraphNodes(e, {
labelFilter: "Process_Unit|Tag|Plant|Site",
relationshipFilter: "WHOLE_PART>"
})
YIELD node as nodes
RETURN Type, e.name, e.description,score,e.source_system, collect(nodes) as Lineage, collect(i.name) AS Issues

Record fields have been truncated. Started streaming 1431 records after 28 ms and completed after 308 ms, displaying first 1000 rows.