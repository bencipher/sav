import os

from dotenv import load_dotenv
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone as PC
from pinecone import Pinecone, ServerlessSpec
from langchain.document_loaders import CSVLoader

load_dotenv()

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"], stage=os.environ["STAGE"])


def create_index(index_name: str = "movie-kg-application") -> None:
    index = None
    try:
        index = pc.Index(index_name)
    except:
        print("Index not found")
        if not index:
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="euclidean",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )


def create_and_save_embeddings(file_path: str, index_name: str = "movie-kg-application",
                               huggingface_embeddings: HuggingFaceInstructEmbeddings = None) -> None:
    loader = CSVLoader(file_path)
    pages = loader.load()

    chunk_size = 2500
    chunk_overlap = 400

    r_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n"]
    )
    splits = r_splitter.split_documents(pages)

    vectorstore = PC.from_documents(splits, huggingface_embeddings, index_name=index_name)
    return vectorstore


def query_movie_vector(query: str, vectorstore: PC, llm) -> None:
    chat_history = []
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    qa = ConversationalRetrievalChain.from_llm(llm, retriever)
    resp = qa.invoke({"question": query, "chat_history": chat_history})
    return resp
