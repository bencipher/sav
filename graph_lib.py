import os

import langchain
from langchain_experimental.graph_transformers import LLMGraphTransformer
from neo4j import GraphDatabase

from config import NODES, RELATIONSHIP
from cypher_text import create_movie_cypher
from prompt_text import CYPHER_GENERATION_TEMPLATE

langchain.debug = True

from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

from dotenv import load_dotenv

load_dotenv()

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)
#
# graph_driver = GraphDatabase.driver(os.environ["LOCAL_NEO4J_URI"],
#                                     auth=(os.environ["LOCAL_NEO4J_USERNAME"], os.environ["LOCAL_NEO4J_PASSWORD"]))
#

graph_driver = GraphDatabase.driver(os.environ["NEO4J_URI"],
                                    auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]))


def query_movie_kb(query: str, graph: Neo4jGraph, llm) -> str:
    chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True, )
    response = chain.invoke({"query": query})
    return response


def create_movie_and_relationships(tx, row):
    genres = row['genres'].split(' ')

    query = create_movie_cypher

    return tx.run(query, index=row["index"], original_title=row['original_title'], budget=int(row['budget']),
                  genres=row['genres'],
                  original_language=row['original_language'], overview=row['overview'], revenue=int(row['revenue']),
                  status=row['status'], title=row['title'], vote_average=float(row['vote_average']),
                  vote_count=int(row['vote_count']), genresList=genres, director=row['director'])


def write_to_graph(df):
    with graph_driver.session() as session:
        for index, row in df.iterrows():
            print(f"Processing row {index}, and row {row}")
            do = create_movie_and_relationships(session, row)
            do.consume()
        print("Done")


def setup_graph_schema(llm):
    return LLMGraphTransformer(
        llm=llm,
        allowed_nodes=NODES,
        allowed_relationships=RELATIONSHIP
    )


def extract_and_save_node(query: str, llm) -> list[str]:
    entities, relationships = setup_graph_schema(llm).extract(query)

    try:
        with graph_driver.session() as session:  # Establish session context
            for entity in entities:
                cypher_query = f"""
                MERGE (n:{entity['label']} {{name: $name}})
                SET n += $properties
                """
                session.run(cypher_query, name=entity['name'], properties=entity['properties'])

            for relationship in relationships:
                cypher_query = f"""
                MATCH (a:{relationship['start_node']['label']} {{name: $start_name}})
                MATCH (b:{relationship['end_node']['label']} {{name: $end_name}})
                MERGE (a)-[r:{relationship['type']}]->(b)
                SET r += $properties
                """
                session.run(
                    cypher_query,
                    start_name=relationship['start_node']['name'],
                    end_name=relationship['end_node']['name'],
                    properties=relationship['properties']
                )

            return True

    except Exception as e:
        print('Error occured while saving: ', e)
        return False


if __name__ == "__main__":
    res = extract_and_save_node(
        "Oluwafemi was the director of Ellipsis, a film that was released in 2018, that grossed 1.2m dollars and was a scifi about africa")
    print(res)
