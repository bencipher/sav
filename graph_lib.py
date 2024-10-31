import os

import langchain
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer

from config import NODES, RELATIONSHIP, graph_driver, get_llm
from cypher_text import create_movie_cypher
from template import CYPHER_GENERATION_TEMPLATE
from utils import create_graph_extract_prompt

langchain.debug = True

from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)
llm = get_llm()

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


def setup_graph_schema():
    transformer = LLMGraphTransformer(
        llm=llm,
        prompt=create_graph_extract_prompt(NODES, RELATIONSHIP),
    )
    return transformer


def make_valid_label(label):
    try:
        if '.' in str(label):
            return f"Value_{str(label).replace('.', '_')}"
        else:
            return f"Value_{int(label)}"
    except ValueError:
        return str(label)


def extract_and_save_node(query: str) -> bool:
    outcome = setup_graph_schema().convert_to_graph_documents([Document(page_content=query)])[0]
    entities, relationships = outcome.nodes, outcome.relationships
    with graph_driver.session() as session:
        for entity in entities:
            label = entity.type
            node_properties = entity.properties
            cypher_query = f"""
            MERGE (n:{label} {{name: $name}})
            """
            if node_properties:
                cypher_query += "SET n += $properties"
            session.run(cypher_query, name=entity.id, properties=node_properties)

        for relationship in relationships:
            cypher_query = f"""
            MATCH (a:{relationship.source.type} {{name: $start_name}})
            MATCH (b:{relationship.target.type} {{name: $end_name}})
            MERGE (a)-[r:{relationship.type}]->(b)
            SET r += $properties
            """
            session.run(
                cypher_query,
                start_name=relationship.source.id,
                end_name=relationship.target.id,
                properties=relationship.properties
            )
    return True


if __name__ == "__main__":
    res = extract_and_save_node(
        "Oluwafemi was the director of Aquaman Africa, a film that was released in 2024, "
        "that grossed 1.2m dollars and was a scifi about africa, it also costed them 500k usd to make",
    )

    print(res)
