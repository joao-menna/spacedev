from langchain_ollama import ChatOllama
import os

local_llm = "llama3.1"

def get_llm() -> ChatOllama:
    model = ChatOllama(
        model=os.environ.get("MODEL", local_llm)
    )

    return model

def get_llm_json() -> ChatOllama:
    model = ChatOllama(
        model=os.environ.get("MODEL", local_llm),
        temperature=0,
        format="json"
    )

    return model