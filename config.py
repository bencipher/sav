import os

from langchain_community.graphs import Neo4jGraph
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()
NODES = {
    "Movie": {
        "properties": [
            "index", "overview", "title",
            "vote_average", "vote_count", "original_title"
        ]
    },
    "Person": {
        "properties": ["director"]
    },
    "Genre": {
        "properties": ["genre"]
    },
    "Budget": {
        "properties": ["budget"]
    },
    "Revenue": {
        "properties": ["revenue"]
    },
    "Status": {
        "properties": ["status"]
    },
    "Language": {
        "properties": ["original_language"]
    }
}

RELATIONSHIP = {
    "DIRECTED": {"from": "Person", "to": "Movie"},
    "IN_GENRE": {"from": "Movie", "to": "Genre"},
    "GROSSED": {"from": "Movie", "to": "Revenue", "weight": 0.8},
    "LANGUAGE_ACTED_IN": {"from": "Movie", "to": "Language", "weight": 0.5},
    "COST": {"from": "Movie", "to": "Budget"},
    "CURRENT_STATUS": {"from": "Movie", "to": "Status", "weight": 1.0}
}

provider = os.environ.get('LLM_PROVIDER', None)
if not provider:
    raise Exception('Set the LLM provider to use, choices between Google or openai in env variable or wherever')
if provider == 'openai':
    llm = ChatOpenAI(model_name='gpt-4o-mini', temperature=0)
elif provider == 'google':
    llm = GoogleGenerativeAI(model='gemini-1.5-pro', temperature=0)

graph = Neo4jGraph()
memory = ConversationBufferMemory(memory_key="chat_history")
graph_driver = GraphDatabase.driver(os.environ["NEO4J_URI"],
                                    auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]))
