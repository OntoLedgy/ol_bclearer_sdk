from neo4j import GraphDatabase
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


#google gen ai
genai.configure(api_key=os.getenv('api_key'))

# model
def answer(question):
    generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    
    prompt_parts = [
    f"you are an expert in neo4j. based on your existing expertise and user conditions you generate cypher query based on the user input. the database has the following nodes CellValue,Sheet,WorkBook. the relation is always from sheets to workbook,cellvalue to sheets and not the otherway around.It has the following relationship type \\\\\\\"is_from\\\\\\\". based on these generate cypher queries based on the user inputs\\\\nmake sure you remove quotes from the response also dont include the word cypher. just give the code only. no special characters\\\\nexample 1 how many sheets are there in total\\\\nresponse : MATCH (s:Sheet)\\\\nRETURN COUNT(s);\\n\\nexample 2 which cell value is related to which sheet and workbook\\\\nresponse : MATCH (c:CellValue)-[r:is_from]->(s:Sheet),(s)-[r1:is_from]->(w:WorkBook)\\\\nRETURN c.value, s.name, w.name;\\nexample 3 how many sheets are  connected to workbook with work_book_title= Temperature Gauge\\\\n\\\\n\\\\n\\\",\\nresponse \\n\\n\\n]\\n\",response MATCH (s:Sheet)-[r:is_from]->(w:WorkBook)\nWHERE w.work_book_title = \"Temperature Gauge\"\nreturn count(s)\n]\n {question}",
    ]
        
    response = model.generate_content(prompt_parts)
    query=response.text
    print(query)
    
    #neo4j connection
    uri = os.getenv('uri')
    username = os.getenv('neo4j_username')
    password = os.getenv('password')
    
    with GraphDatabase.driver(uri,auth=(username,password)) as driver:
        with driver.session() as session:
            result = session.run(query)
            for record in result:
                print(record)


answer("how many workbooks are there")
