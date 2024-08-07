import os

from dotenv import load_dotenv
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from typing import List

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

from graph_lib import extract_and_save_node
from template import CYPHER_TEMPLATE

load_dotenv()

llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
graph = Neo4jGraph(url=os.environ["NEO4J_URI"], username=os.environ["NEO4J_USERNAME"],
                   password=os.environ["NEO4J_PASSWORD"], database="neo4j")


#
# class MovieSearchTool(BaseTool):
#     name: str = "search_movie_knowledge_graph"
#     description: str = """
#         Useful for when you need information about movies.
#         Input should be a search query.
#         Returns a list of search result movies or associated information.
#     """
#
#     args_schema: Type[BaseModel] = MovieQuery
#
#     def _run(
#             self,
#             query: str,
#             run_manager: Optional[CallbackManagerForToolRun] = None,
#     ) -> dict[str]:
#         """Use the tool."""
#         cypher_prompt = PromptTemplate(
#             input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
#         )
#         chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True, prompt_text=cypher_prompt)
#         print("cypher prompt: ", chain.cypher_generation_chain.prompt)
#
#         response = chain.invoke({"query": query})
#         return response
#
#     def _arun(
#             self,
#             *args: Any,
#             **kwargs: Any,
#     ) -> Any:
#         raise NotImplementedError


def movie_search_tool(query: str):
    """Use the tool."""
    cypher_prompt = PromptTemplate(
        input_variables=["schema", "question"], template=CYPHER_TEMPLATE
    )
    chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True, prompt_text=cypher_prompt)

    response = chain.invoke({"query": query})
    return response


def save_extra_info(query: str) -> List[str]:
    if extract_and_save_node(query, llm):
        return ["Saved extra information"]

    return ["I can't save extra information at the moment"]
