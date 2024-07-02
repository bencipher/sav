import os
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain_community.graphs import Neo4jGraph
from langchain_community.memory.kg import ConversationKGMemory
from langchain_google_genai import GoogleGenerativeAI

from neo4j import GraphDatabase, READ_ACCESS
from tools import MovieSearchTool, save_extra_info

load_dotenv()

llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
tools = [
    # MovieSearchTool(),
    Tool(
        name="Save Extra Information",
        func=save_extra_info,
        description="Saves extra information extracted from the conversation."
    )
]

memory = ConversationKGMemory(llm=llm)

# Create the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent_type="zero-shot-react-description",
    verbose=True,
    return_intermediate_steps=True,
)


def run_agent(query: str):
    return agent.invoke({"input": query})


# Run the Chainlit app
if __name__ == "__main__":
    query = "Tell me about the movie Inception."
    response = run_agent(query)

    st.title("Movie Knowledge Graph Chat")

    query = st.text_input("Enter your question about movies:")

    if st.button("Send"):
        if query:
            response = run_agent(query)
            st.text(response["output"])
    #
    print(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"], os.environ["NEO4J_URI"], )
    graph_driver = GraphDatabase.driver(os.environ["NEO4J_URI"],
                                        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]))
    print(graph_driver)
    try:
        graph = Neo4jGraph(url=os.environ["LOCAL_NEO4J_URI"], user=os.environ["LOCAL_NEO4J_USERNAME"],
                           password="password", database="neo4j")

        # graph = Neo4jGraph()
    except Exception as e:
        print(e)
