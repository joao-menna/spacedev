from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import os


def get_llm():
    provider = os.environ.get("PROVIDER", "ollama")

    if provider == "ollama":
        model = ChatOllama(
            model=os.environ.get("MODEL", "llama3.1"),
            temperature=0.7
        )

    if provider == "openai":
        model = ChatOpenAI(
            model=os.environ.get("MODEL", "gpt-4o"),
            temperature=0.7,
        )

    return model


def get_llm_json() -> ChatOllama:
    model = ChatOllama(
        model=os.environ.get("MODEL", local_llm), temperature=0, format="json"
    )

    return model
