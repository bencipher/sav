import streamlit as st
from dotenv import load_dotenv
from langchain.agents import Tool, LLMSingleActionAgent, AgentExecutor
from langchain.chains.llm import LLMChain

from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted
import tiktoken
from langchain.memory import ConversationBufferWindowMemory

from custom_prompts import CustomPromptTemplate
from parser import CustomOutputParser
from template import AGENT_TEMPLATE
import langchain

langchain.debug = False

from tools import save_extra_info, movie_search_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
tools = [
    # MovieSearchTool(),
    Tool(
        name="Save Extra Information",
        func=save_extra_info,
        description="Saves new information the user wants us to know about movies we don't know about",
    ),
    Tool(
        name="Search All Movie Informations",
        func=movie_search_tool,
        description="Useful for when you need information about movies. Input should be a search query. Returns a list of search result links to be scraped"
    )
]

prompt = CustomPromptTemplate(
    template=AGENT_TEMPLATE,
    tools=tools,
    input_variables=["input", "intermediate_steps", "history"]
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

tool_names = [tool.name for tool in tools]
output_parser = CustomOutputParser()

agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=tool_names
)
memory = ConversationBufferWindowMemory(k=3)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent,
                                                    tools=tools,
                                                    memory=memory,
                                                    verbose=True)


def run_agent(query: str):
    encoding = tiktoken.encoding_for_model("gpt-4")
    input_tokens = encoding.encode(query)
    resp = agent_executor.run(query)
    output_tokens = encoding.encode(resp)
    st.write(f"Input token count: {len(input_tokens)}")
    st.write(f"Output token count: {len(output_tokens)}")
    return resp


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
                st.session_state.history.append({"query": query, "response": response})
            except ResourceExhausted as e:
                st.text("I have so many requests, please hold on while I generate your response...")
                response = run_agent(query)
                st.session_state.history.append({"query": query, "response": response})

    # Display the last 7 messages
    for message in st.session_state.history[-7:]:
        st.text(f"User: {message['query']}")
        st.text(f"Bot: {message['response']}")
