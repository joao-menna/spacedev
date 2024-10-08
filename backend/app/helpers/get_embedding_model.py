from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
import os


def get_embedding_model():
    provider = os.environ.get("PROVIDER_EMBEDDING_MODEL", "ollama")

    if provider == "ollama":
        model = OllamaEmbeddings(
            model=os.environ.get("EMBEDDING_MODEL", "nomic-embed-text")
        )

    if provider == "openai":
        model = OpenAIEmbeddings(
            model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
        )

    return model
