import os
from pprint import pprint
import langchain
import tiktoken
import streamlit as st
from langchain.agents import LLMSingleActionAgent, AgentExecutor
from langchain.schema import StrOutputParser
from langchain.agents import create_react_agent

from config import create_llm, memory
from parser import CustomOutputParser
from prompts import CustomPromptTemplate
from template import AGENT_TEMPLATE
from tools import initialize_tools


st.set_page_config(page_title="IMDB Chat", page_icon=":robot:")
st.title("Get any info about classic 21st century movies")
model = st.selectbox(
    "Select the model to use:", ["Default", "Gemini", "OpenAI"]
).lower()
if model in ["openai", "gemini"]:
    api_key = st.text_input(
        "Enter your API Key:",
        type="password",
        placeholder="paste your api key here",
    )
    if not api_key:
        st.warning("Please enter your API Key to proceed.")
        st.stop()

    llm = create_llm(model, api_key)
else:
    llm = create_llm()

if "llm" not in st.session_state:
    st.session_state.llm = None
if "history" not in st.session_state:
    st.session_state.history = []
st.session_state.llm = llm


langchain.debug = os.environ.get('DEBUG')
output_parser = CustomOutputParser()

tools = initialize_tools(llm)

prompt = CustomPromptTemplate(
    input_variables=[
        "input",
        "chat_history",
        "agent_scratchpad",
        "tools",
        "tool_names",
    ],
    template=AGENT_TEMPLATE,
    tools=tools,
    # partial_variables={"tools": tools, "tool_names": [tool.name for tool in tools]},
)

agent = create_react_agent(
    llm,
    tools,
    prompt,
    # stop_sequence=["\nObservation"],
    output_parser=CustomOutputParser(),
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    memory=memory,
)

def run_agent(question: str) -> str:
    encoding = tiktoken.encoding_for_model("gpt-4")
    input_tokens = encoding.encode(question)
    # res = agent_executor.invoke(input=question)
    res = agent_executor.invoke({"input": question}).get("output")
    pprint(res)
    output_tokens = encoding.encode(res)
    pprint(f"Input token: {len(input_tokens)}\nOutput token: {len(output_tokens)}")
    return res or "Too many requests, please reload and try again later"


if query := st.chat_input(
    placeholder="ask your question e.g. how much did invictus gross and what was the rating?",
):
    st.session_state.history.append({"role": "user", "content": query})
    # response = run_agent(query)
    # st.session_state.history.append({"role": "assistant", "content": response})
    try:
        response = run_agent(query)
        st.session_state.history.append({"role": "assistant", "content": response})
    except Exception as e:
        print(str(e))
        st.text("Please confirm that you have tokens left on your quota...")

for msg in st.session_state.history:
    st.chat_message(msg["role"]).write(msg["content"])
