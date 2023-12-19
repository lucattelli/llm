import logging

from llm.shared.logger import configure_logger
from myrag.openai import rag

configure_logger()

logger = logging.getLogger(__name__)

logger.info("Running query....")
results = rag.run_query("sci-fi movie in space")
for movie in results:
    logger.info("Movie '%s' found with plot '%s'", movie["title"], movie["plot"])
