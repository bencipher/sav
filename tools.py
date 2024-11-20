import os
from langchain_core.prompts import PromptTemplate
from langchain.chains import GraphCypherQAChain
from langchain.agents import Tool
from config import graph
from graph_lib import extract_and_save_node


from template import CYPHER_GENERATION_TEMPLATE, QA_TEMPLATE


def initialize_tools(llm):
    """Initialize tools with the provided LLM and return them along with the chain."""
    cypher_prompt = PromptTemplate(
        input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
    )
    qa_prompt = PromptTemplate(
        input_variables=["context", "question"], template=QA_TEMPLATE
    )

    chain = GraphCypherQAChain.from_llm(
        graph=graph,
        llm=llm,
        verbose=True,
        prompt_text=cypher_prompt,
        allow_dangerous_requests=True,
        # qa_prompt=qa_prompt,
    )

    def movie_search_tool(query: str):
        response = chain.invoke({"query": query})
        return response

    def save_extra_info(query: str) -> bool:
        return extract_and_save_node(llm=llm, query=query)

    tools = [
        Tool(
            name="Save Extra Information",
            func=save_extra_info,
            description="Saves new information the user wants us to know about movies we don't know about",
        ),
        Tool(
            name="Search All Movie Information",
            func=movie_search_tool,
            description="""Useful for when you need information about movies. 
                        should be a search query. Returns a list of search result of movies information in the knowledge base""",
        ),
    ]

    return tools
