import os
from typing import Optional
import streamlit as st

from langchain_community.graphs import Neo4jGraph
from neo4j import GraphDatabase

from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()


# NODES = {
#     "Movie": {
#         "properties": [
#             "index",
#             "overview",
#             "title",
#             "vote_average",
#             "vote_count",
#             "original_title",
#         ]
#     },
#     "Person": {"properties": ["director"]},
#     "Genre": {"properties": ["genre"]},
#     "Budget": {"properties": ["budget"]},
#     "Revenue": {"properties": ["revenue"]},
#     "Status": {"properties": ["status"]},
#     "Language": {"properties": ["original_language"]},
# }

# RELATIONSHIP = {
#     "DIRECTED": {"from": "Person", "to": "Movie"},
#     "IN_GENRE": {"from": "Movie", "to": "Genre"},
#     "GROSSED": {"from": "Movie", "to": "Revenue", "weight": 0.8},
#     "LANGUAGE_ACTED_IN": {"from": "Movie", "to": "Language", "weight": 0.5},
#     "COST": {"from": "Movie", "to": "Budget"},
#     "CURRENT_STATUS": {"from": "Movie", "to": "Status", "weight": 1.0}
# }

NODES = {
    "Movie": {
        "properties": [
            "index",
            "overview",
            "title",
            "vote_average",
            "vote_count",
        ]
    },
    "Person": {"properties": ["director", "name"]},
    "Genre": {"properties": ["genre", "name"]},
    "Budget": {"properties": ["budget", "amount"]},
    "Revenue": {"properties": ["revenue", "amount"]},
    "Status": {"properties": ["status", "name"]},
    "Language": {"properties": ["original_language", "name"]},
}

RELATIONSHIP = {
    "DIRECTED": {
        "from": "Person",
        "to": "Movie",
        "target_node_id": "movie_id",
    },  # Added target_node_id
    "IN_GENRE": {
        "from": "Movie",
        "to": "Genre",
        "target_node_id": "genre_id",
    },  # Added target_node_id
    "GROSSED": {
        "from": "Movie",
        "to": "Revenue",
        "weight": 0.8,
        "target_node_id": "revenue_id",
    },  # Added target_node_id
    "LANGUAGE_ACTED_IN": {
        "from": "Movie",
        "to": "Language",
        "weight": 0.5,
        "target_node_id": "language_id",
    },  # Added target_node_id
    "COST": {
        "from": "Movie",
        "to": "Budget",
        "target_node_id": "budget_id",
    },  # Added target_node_id
    "CURRENT_STATUS": {
        "from": "Movie",
        "to": "Status",
        "weight": 1.0,
        "target_node_id": "status_id",
    },  # Added target_node_id
}

def create_llm(model: Optional[str] = None, api_key: Optional[str] = None):
    """Factory function to create the LLM based on the selected model."""
    if model == "openai":
        return ChatOpenAI(model_name="gpt-4o-mini", temperature=0, api_key=api_key)
    elif model == "gemini":
        return GoogleGenerativeAI(
            model="gemini-1.5-pro", temperature=0, api_key=api_key
        )
    else:
        return ChatGroq(
            model="gemma2-9b-it",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=3,
            streaming=True,
            api_key=os.environ.get("GROQ_API_KEY"),
        )


def get_llm():
    return st.session_state.llm


graph_driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
)


def test_connection():
    try:
        with graph_driver.session() as session:
            result = session.run("RETURN 1")
            print("Connection successful:", result.single())
    except Exception as e:
        print("Connection failed:", e)
    finally:
        graph_driver.close()


graph = Neo4jGraph(
    url=os.environ["NEO4J_URI"],
    username=os.environ["NEO4J_USERNAME"],
    password=os.environ["NEO4J_PASSWORD"],
)


def test_graph():
    try:
        result = graph.query("RETURN 1 AS test")
        print("Graph Connection successful:", result, graph.get_schema)
    except Exception as e:
        print("Connection failed:", e)


test_connection()
test_graph()

memory = ConversationBufferMemory(memory_key="chat_history")
