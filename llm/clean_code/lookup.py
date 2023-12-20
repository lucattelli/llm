from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain.llms.openai import OpenAI
from langchain.chains import RetrievalQA

from llm.shared.mongo import get_collection
from llm.shared.settings import Secrets


def lookup_embeddings(query: str) -> tuple[str, any]:
    collection = get_collection("llm", "clean_code")
    secrets = Secrets()
    embeddings = OpenAIEmbeddings(api_key=secrets.openai_api_key)
    vector_store = MongoDBAtlasVectorSearch(collection, embeddings)

    docs = vector_store.similarity_search(query, k=1)
    content = docs[0].page_content

    llm = OpenAI(api_key=secrets.openai_api_key, temperature=0)
    retriever = vector_store.as_retriever()
    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)

    answer = qa.run(query)

    return content, answer
