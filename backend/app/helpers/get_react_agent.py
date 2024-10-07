from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent, ToolNode
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
from typing import Annotated
from app.helpers.get_chroma import get_chroma
from app.helpers.get_llm import get_llm

system_prompt = """
Your name is SpaceDev.
Learn and interpret the code in the context, later you may be prompted to explain this code or recover it.
You will be used as a knowledge base, you are a helpful assistant that answer in the same language that you were asked the question.
Only use the sources provided in the context. If there are no sources, do not write any json for the sources. If there are sources, separated by four new lines, without saying they are sources, without wrapping in markdown code block, you will display the sources in a json format, containing the key "sources", it always being an array of strings, the strings will be the sources from the context you used to reach the response.

Example with sources (where your_response is your response):
<example_with_sources>
<your_response />

{{
  "sources": [
    "Wiki - How to make a RAG",
    "Wiki - How to index a document in a vector store",
    "/home/user/app/backend/file.py"
  ]
}}
</example_with_sources>

<context>
{context}
</context>
"""


class State(TypedDict):
    messages: Annotated[list, add_messages]


def format_docs(docs):
    context = ""

    for doc in docs:
        context += "Source: " + doc.metadata["source"]
        context += "\n\n"
        context += doc.page_content
        context += "\n\n---\n\n"

    return context


@tool
def get_documents(keywords: str) -> list[Document]:
    """Use this to get documents through keywords separated by space."""
    vector_store = get_chroma()
    retriever = vector_store.as_retriever(search_type="mmr")

    docs = retriever.invoke(keywords)
    return docs


def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]

    if not last_message.tool_calls:
        return END
    else:
        return "tools"


async def call_model(state: State, config: RunnableConfig):
    messages = state["messages"]
    response = await model.ainvoke(messages, config)

    return {"messages": response}


model = get_llm()

tools = [get_documents]

tool_node = ToolNode(tools)

model.bind_tools(tools)


workflow = StateGraph(State)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    ["tools", END],
)

workflow.add_edge("tools", "agent")

app = workflow.compile()


def get_chat_chain():
    return app
