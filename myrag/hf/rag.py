import logging
from time import sleep

import pymongo
import requests
from pymongo.collection import Collection

from llm.shared.settings import Secrets, Settings

secrets = Secrets()
settings = Settings()
logger = logging.getLogger(__name__)

BACKOFF = 5


def __get_mongo_collection() -> Collection:
    logger.debug("Connecting to Mongo")
    client = pymongo.MongoClient(secrets.mongo_uri)
    db = client.sample_mflix
    logger.debug("Returning collection movies")
    return db.get_collection("movies")


def __perform_request(text: str):
    return requests.post(
        settings.huggingface_embedding_url,
        headers={"Authorization": f"Bearer {secrets.huggingface_access_token}"},
        json={"inputs": text},
        timeout=60,
    )


def __generate_embedding(text: str) -> list[float]:
    logger.debug("Generating embedding", extra={"text": text})
    response = __perform_request(text)
    additional_backoff = BACKOFF
    if response.status_code == 503:
        logger.error("Rate-limited by Huggingface API, trying again after backoff")
        additional_backoff += BACKOFF
        sleep(additional_backoff)
        logger.debug("Retrying after backoff")
        response = __perform_request(text)
        response.raise_for_status()

    embedding = response.json()
    logger.debug("Embedding successfully generated", extra={"embedding": embedding})
    return embedding


def generate_embeddings(limit: int) -> None:
    collection = __get_mongo_collection()

    logger.debug("Querying Mongo for movies without embeddings")
    items = collection.find(
        {"plot": {"$exists": True}, "plot_embedding_hf": {"$exists": False}}
    ).limit(limit)

    logger.debug("Initiating embedding generation for Mongo results")
    for doc in items:
        logger.debug("Generating embeddings for movie %s", doc["title"])
        doc["plot_embedding_hf"] = __generate_embedding(doc["plot"])
        collection.replace_one({"_id": doc["_id"]}, doc)
        sleep(BACKOFF)
    logger.debug("Completed embedding generation for Mongo results")


def run_query(query: str) -> list[dict]:
    collection = __get_mongo_collection()

    logger.debug("Running query for '%s'", query)
    results = collection.aggregate(
        [
            {
                "$vectorSearch": {
                    "queryVector": __generate_embedding(query),
                    "path": "plot_embedding_hf",
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
