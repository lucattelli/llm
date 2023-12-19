from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch

from llm.shared.mongo import get_collection
from llm.shared.settings import Secrets


def ingest_book(file_path: str):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()

    collection = get_collection("llm", "clean_code")

    secrets = Secrets()
    embeddings = OpenAIEmbeddings(api_key=secrets.openai_api_key)

    MongoDBAtlasVectorSearch.from_documents(
        documents=pages,
        embedding=embeddings,
        collection=collection,
    )
