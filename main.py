import os
from dotenv import set_key, load_dotenv
import requests
# Load environment variables from .env file if it exists
import streamlit as st
import langchain
from dotenv import load_dotenv
from langchain.agents import LLMSingleActionAgent, AgentExecutor
from langchain.chains.llm import LLMChain

import tiktoken

from config import memory, llm
from parser import CustomOutputParser
from prompts import CustomPromptTemplate
from template import AGENT_TEMPLATE
from tools import tools

load_dotenv()

langchain.debug = os.environ.get('DEBUG')
output_parser = CustomOutputParser()

prompt = CustomPromptTemplate(
    input_variables=["input", "chat_history", "intermediate_steps"],
    template=AGENT_TEMPLATE,
    tools=tools,
)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=LLMSingleActionAgent(
        llm_chain=langchain.chains.LLMChain(llm=llm, prompt=prompt),
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=[tool.name for tool in tools],
    ),
    tools=tools,
    verbose=True,
    memory=memory
)


def run_agent(query: str):
    encoding = tiktoken.encoding_for_model("gpt-4")
    input_tokens = encoding.encode(query)
    response = agent_executor.invoke(input=query)
    output_tokens = encoding.encode(response)
    st.write(f"Input token count: {len(input_tokens)}")
    st.write(f"Output token count: {len(output_tokens)}")
    return response


def set_environment_variable(key, value):
    # Set the environment variable in .env file
    set_key(".env", key, value)
    os.environ[key] = value


def validate_api_key(key: str, llm_model: str):
    if llm_model.lower() == "openai":
        headers = {"Authorization": f"Bearer {key}"}
        res = requests.get("https://api.openai.com/v1/models", headers=headers)
        return res.status_code == 200
    elif llm_model.lower() == "gemini":
        headers = {"Authorization": f"Bearer {key}"}
        res = requests.get("https://api.gemini.com/v1/validate", headers=headers)
        return res.status_code == 200
    return False


if __name__ == "__main__":
    st.set_page_config(page_title="IMDB Chat", page_icon=":robot:")
    st.title("Get any info about classic 21st century movies")
    model = st.selectbox("Select the model to use:", ["Gemini", "OpenAI"])
    api_key = st.text_input("Enter your API Key:", type="password")

    if "history" not in st.session_state:
        st.session_state.history = []

    query = st.text_input("Chat with the IMDB AI")

    if st.button("Send"):
        if api_key:
            set_environment_variable("API_KEY", api_key)
            set_environment_variable("MODEL", model)
            if validate_api_key(api_key, model):
                st.success("API Key and model have been set and validated successfully.")
            else:
                st.error("Invalid API Key or insufficient tokens. Please check and try again.")
        else:
            st.error("Please enter a valid API Key for your selected model.")
        if query:
            try:
                response = run_agent(query)
                st.session_state.history.append({"query": query, "response": response})
            except Exception as e:
                st.text("Please confirm that you have tokens left on your quota...")
                response = run_agent(query)
                st.session_state.history.append({"query": query, "response": response})

    # Display the last 7 messages
    for message in st.session_state.history[-7:]:
        st.text(f"User: {message['query']}")
        st.text(f"Bot: {message['response']}")
