import os
from pprint import pprint
import langchain
import tiktoken
import streamlit as st
from langchain.agents import LLMSingleActionAgent, AgentExecutor
from langchain.chains.llm import LLMChain


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
    memory=memory,
    show_intermediate_steps=True,
)


def run_agent(question: str) -> str:
    encoding = tiktoken.encoding_for_model("gpt-4")
    input_tokens = encoding.encode(question)
    res = agent_executor.invoke(input=question).get("output")
    output_tokens = encoding.encode(res)
    pprint(f"Input token: {len(input_tokens)}\nOutput token: {len(output_tokens)}")
    return res


if query := st.chat_input("Chat with the IMDB AI"):
    st.session_state.history.append({"role": "user", "content": query})
    try:
        response = run_agent(query)
        st.session_state.history.append({"role": "assistant", "content": response})
    except Exception as e:
        st.text("Please confirm that you have tokens left on your quota...")

for msg in st.session_state.history:
    st.chat_message(msg["role"]).write(msg["content"])
