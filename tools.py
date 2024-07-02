import os

from dotenv import load_dotenv
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Type, Optional, List, Any

from langchain_google_genai import GoogleGenerativeAI

from models import MovieQuery

load_dotenv()


llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
graph = Neo4jGraph(url=os.environ["NEO4J_URI"], username=os.environ["NEO4J_USERNAME"],
                   password=os.environ["NEO4J_PASSWORD"], database="neo4j")

class MovieSearchTool(BaseTool):
    name: str = "search_movie_knowledge_graph"
    description: str = """
        Useful for when you need information about movies. 
        Input should be a search query.
        Returns a list of search result links to be scraped.
    """

    args_schema: Type[BaseModel] = MovieQuery

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict[str]:
        """Use the tool."""

        chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True)
        response = chain.invoke({"query": query})
        return response

    def _arun(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        raise NotImplementedError


def save_extra_info(query: str) -> List[str]:
    pass
