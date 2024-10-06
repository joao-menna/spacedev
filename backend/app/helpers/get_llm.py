from langchain_ollama import OllamaLLM
import os

def get_llm() -> OllamaLLM:
    model = OllamaLLM(
        model=os.environ.get("MODEL", "llama3.1")
    )

    return model