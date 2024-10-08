from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain.chains.retrieval import create_retrieval_chain
from langchain.tools.retriever import create_retriever_tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, create_react_agent
from typing_extensions import Annotated, TypedDict
from app.helpers.get_chroma import get_chroma
from app.helpers.get_llm import get_llm
from typing import Sequence


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    tool_already_called: str


system_prompt = """
Your name is SpaceDev. Learn the code in the context, later you may be prompted to explain this code, recover it or talk about it.
You will be used as a knowledge base, you are a helpful assistant that answer in the same language that you were asked the question.
Only use the sources provided in the context. Separated by four new lines, without saying they are sources, without wrapping in markdown code block, you will display the sources in a JSON format, containing the key "sources", it always being an array of strings, the strings will be the sources from the context you used to reach the response.
Answer in the user's language. And if you do not know the answer, say that you do not know.
You do not need to display the source content.

Example with sources (where <your_response /> is your own response):
<example_with_sources>
<your_response />

{{
  "sources": [
    "Wiki - How to make a RAG",
    "Wiki - How to index a document in a vector store",
    "/mnt/data/project/backend/main.py"
  ]
}}
</example_with_sources>

<context>
{context}
</context>

<chat_history>
{chat_history}
</chat_history>
"""

vector_store = get_chroma()
retriever = vector_store.as_retriever(search_type="mmr")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ],
)


def format_docs(docs):
    context = ""

    for doc in docs:
        context += "Source: " + doc.metadata["source"]
        context += "\n\n"
        context += doc.page_content
        context += "\n\n"

    return context


@tool
def retrieve_documents(keywords: str):
    """Retrieve documents from a codebase to answer the user's question. Pass keywords as parameter, separated by space."""
    docs = retriever.invoke(keywords)

    return format_docs(docs)



tools = [retrieve_documents]

tool_node = ToolNode(tools)

model = get_llm().bind_tools(tools)


async def call_model(state: State, config: RunnableConfig):
    messages = state["messages"]
    response = await model.ainvoke(messages, config)
    return {
        "messages": [response],
    }


async def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tools"

    return END


workflow = StateGraph(State)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges("agent", should_continue)

workflow.add_edge("tools", "agent")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def get_chat_chain():
    return app
