import os

from neo4j import GraphDatabase

uri = ""
username = ""
password = ""


def execute_query_from_file(file_path):
    with open(file_path) as file:
        query = file.read()
        with GraphDatabase.driver(
            uri,
            auth=(username, password),
        ) as driver:
            with driver.session() as session:
                result = session.run(
                    query,
                )
                for record in result:
                    print(record)


cypher_scripts_folder = r"C:\Users\Ramanathan.TRB\Shell\Khan, Mesbah A GSUK-PTX D F - bCLEARerProjects\RDL\DEP\03 - Evolve\cypher_queries"
for filename in os.listdir(
    cypher_scripts_folder,
):
    if filename.endswith(".cypher"):
        script_path = os.path.join(
            cypher_scripts_folder,
            filename,
        )
        print(
            f"Executing script: {script_path}",
        )
        execute_query_from_file(
            script_path,
        )
