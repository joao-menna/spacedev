from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from app.helpers.get_chroma import get_chroma
from app.helpers.get_llm import get_llm

system_prompt = """
Your name is SpaceDev.
Learn and interpret the code in the context, later you may be prompted to explain this code or recover it.
You will be used as a knowledge base, you are a helpful assistant that answer in the same language that you were asked the question.
Only use the sources provided in the context. If there are no sources, do not write any json for the sources. If there are sources, separated by four new lines, without saying they are sources, without wrapping in markdown code block, you will display the sources in a json format, containing the key "sources", it always being an array of strings, the strings will be the sources from the context you used to reach the response.

Example response with sources:
<example_response_with_sources>
Hello, I'm SpaceDev! Nice to meet you!


{{
  "sources": [
    "Wiki - How to make a RAG",
    "Wiki - How to index a document in a vector store"
  ]
}}
</example_response_with_sources>

Example response without sources:
<example_response_without_sources>
Hello, I'm SpaceDev! Nice to meet you!


{{
  "sources": []
}}
</example_response_without_sources>

<context>
{context}
</context>

Answer the following question:

{question}
"""


def format_docs(docs):
    context = ""

    for doc in docs:
        context += "Source: " + doc.metadata["source"]
        context += "\n\n"
        context += doc.page_content
        context += "\n\n"

    return context


def get_chat_chain():
    vector_store = get_chroma()
    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_template(system_prompt)

    model = get_llm()

    chain = (
        { "context": retriever | format_docs, "question": RunnablePassthrough() }
        | prompt
        | model
        | StrOutputParser()
    )

    return chain