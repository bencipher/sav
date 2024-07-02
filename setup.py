import os

import pandas as pd
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain_google_genai import GoogleGenerativeAI

from graph_lib import setup_graph_schema, write_to_graph
from vector import create_index, create_and_save_embeddings

load_dotenv()

llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
huggingface_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")

file_path = os.environ['DATA_PATH']


# create the graph schema and load data into it
def setup_graph_kb():
    df = pd.read_csv(file_path)
    setup_graph_schema(llm)
    write_to_graph(df)


# create the vector store and embeddings
def setup_vector_store():
    create_index()
    create_and_save_embeddings(file_path=file_path, huggingface_embeddings=huggingface_embeddings)


# This should be run once to create the vector store and graph
if __name__ == "__main__":
    setup_graph_kb()
    # setup_vector_store()
