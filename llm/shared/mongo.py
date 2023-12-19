from pymongo import MongoClient
from pymongo.database import Database

from llm.shared.settings import Secrets


def get_collection(database: str, collection: str) -> Database:
    secrets = Secrets()
    client = MongoClient(secrets.mongo_uri)
    return client[database][collection]
