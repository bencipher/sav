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


NODES = {
    "Movie": {
        "properties": [
            "index",
            "overview",
            "title",
            "vote_average",
            "vote_count",
            "original_title",
        ]
    },
    "Person": {"properties": ["director"]},
    "Genre": {"properties": ["genre"]},
    "Budget": {"properties": ["budget"]},
    "Revenue": {"properties": ["revenue"]},
    "Status": {"properties": ["status"]},
    "Language": {"properties": ["original_language"]},
}

RELATIONSHIP = {
    "DIRECTED": {"from": "Person", "to": "Movie"},
    "IN_GENRE": {"from": "Movie", "to": "Genre"},
    "GROSSED": {"from": "Movie", "to": "Revenue", "weight": 0.8},
    "LANGUAGE_ACTED_IN": {"from": "Movie", "to": "Language", "weight": 0.5},
    "COST": {"from": "Movie", "to": "Budget"},
    "CURRENT_STATUS": {"from": "Movie", "to": "Status", "weight": 1.0}
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


graph = Neo4jGraph()
graph_driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
)

memory = ConversationBufferMemory(memory_key="chat_history")
