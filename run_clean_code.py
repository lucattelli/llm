from llm.clean_code.ingestion import ingest_book
from llm.clean_code.lookup import lookup_embeddings
from llm.shared.logger import configure_logger

configure_logger()


ingest_book("llm/clean_code/robert-c-martin_clean-code.pdf")

content, output = lookup_embeddings("how to write clean functions")

print("CONTENT", content)
print("OUTPUT", output)
