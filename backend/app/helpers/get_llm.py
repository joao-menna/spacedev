from langchain_ollama import ChatOllama
import os

def get_llm() -> ChatOllama:
    model = ChatOllama(
        model=os.environ.get("MODEL", "llama3.1"),
    )

    return model