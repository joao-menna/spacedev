from langchain_chroma import Chroma
from app.helpers.get_embedding_model import get_embedding_model
import os


def get_chroma() -> Chroma:
    persist_directory = os.path.abspath(os.path.join(os.getcwd(), "chroma"))

    vector_store = Chroma(
        collection_name="spacedev",
        embedding_function=get_embedding_model(),
        persist_directory=persist_directory,
    )

    return vector_store
