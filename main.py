import os

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

langchain.debug = os.environ.get('DEBUG')
load_dotenv()

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

#
# # Run the Chainlit app
# if __name__ == "__main__":
#     st.set_page_config(page_title="Movie Knowledge Graph Chat", page_icon=":robot:")
#     st.title("Movie Knowledge Graph Chat")
#
#     if "history" not in st.session_state:
#         st.session_state.history = []
#
#     query = st.text_input("Enter your question about movies:")
#
#     if st.button("Send"):
#         if query:
#             try:
#                 response = run_agent(query)
#                 st.session_state.history.append({"query": query, "response": response})
#             except ResourceExhausted as e:
#                 st.text("I have so many requests, please hold on while I generate your response...")
#                 response = run_agent(query)
#                 st.session_state.history.append({"query": query, "response": response})
#
#     # Display the last 7 messages
#     for message in st.session_state.history[-7:]:
#         st.text(f"User: {message['query']}")
#         st.text(f"Bot: {message['response']}")
