import os
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain_community.graphs import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted
from langchain import PromptTemplate
import tiktoken
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from prompt_text import agent_prompt_template
import langchain

langchain.debug = True

from neo4j import GraphDatabase, READ_ACCESS
from tools import MovieSearchTool, save_extra_info

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
tools = [
    MovieSearchTool(),
    Tool(
        name="Save Extra Information",
        func=save_extra_info,
        description="Saves new information the user wants us to know about movies we don't know about",
    )
]

memory = ConversationBufferWindowMemory(memory_key='chat_history', k=3, return_messages=True)
prompt_template = PromptTemplate(
    input_variables=["agent_scratchpad", "input"],
    template=agent_prompt_template)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent_type="chat-conversational-react-description",
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True,
    early_stopping_method='generate',
    prompt=prompt_template,
    max_iterations=2,
)


def run_agent(query: str):
    encoding = tiktoken.encoding_for_model("gpt-4")
    input_tokens = encoding.encode(query)
    response = agent.invoke({"input": query})
    output_tokens = encoding.encode(response["output"])
    st.write(f"Input token count: {len(input_tokens)}")
    st.write(f"Output token count: {len(output_tokens)}")
    return response


# Run the Chainlit app
if __name__ == "__main__":
    st.set_page_config(page_title="Movie Knowledge Graph Chat", page_icon=":robot:")
    st.title("Movie Knowledge Graph Chat")

    if "history" not in st.session_state:
        st.session_state.history = []

    query = st.text_input("Enter your question about movies:")

    if st.button("Send"):
        if query:
            try:
                response = run_agent(query)
                st.session_state.history.append({"query": query, "response": response["output"]})
            except ResourceExhausted as e:
                st.text("I have so many requests, please hold on while I generate your response...")
                response = run_agent(query)
                st.session_state.history.append({"query": query, "response": response["output"]})

    # Display the last 7 messages
    for message in st.session_state.history[-7:]:
        st.text(f"User: {message['query']}")
        st.text(f"Bot: {message['response']}")
