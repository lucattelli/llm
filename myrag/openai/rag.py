import logging

import openai
import pymongo
from pymongo.collection import Collection

from llm.shared.settings import Secrets, Settings

secrets = Secrets()
settings = Settings()
logger = logging.getLogger(__name__)


def __get_mongo_collection() -> Collection:
    logger.debug("Connecting to Mongo")
    client = pymongo.MongoClient(secrets.mongo_uri)
    db = client.sample_mflix
    logger.debug("Returning collection embedded_movies")
    return db.get_collection("embedded_movies")


def __generate_embedding(text: str) -> list[float]:
    openai.api_key = secrets.openai_api_key
    logger.debug("Generating embedding", extra={"text": text})
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text,
    )
    embedding = response.data[0].embedding
    logger.debug("Embedding successfully generated", extra={"embedding": embedding})
    return embedding


def run_query(query: str) -> list[dict]:
    collection = __get_mongo_collection()
    logger.debug("Running query for '%s'", query)
    results = collection.aggregate(
        [
            {
                "$vectorSearch": {
                    "queryVector": __generate_embedding(query),
                    "path": "plot_embedding",
                    "numCandidates": 100,
                    "limit": 4,
                    "index": "PlotSemanticSearch",
                }
            }
        ]
    )
    movies = list(results)
    logger.debug("Found %d items", len(movies))
    return movies
