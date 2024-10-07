from langchain_ollama import OllamaEmbeddings
import os


def get_embedding_model() -> OllamaEmbeddings:
    model = OllamaEmbeddings(
        model=os.environ.get("EMBEDDING_MODEL", "nomic-embed-text")
    )

    return model
