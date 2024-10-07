from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from typing_extensions import Annotated, TypedDict
from langgraph.graph.message import add_messages
from app.helpers.get_chroma import get_chroma
from app.helpers.get_llm import get_llm
from typing import Sequence


class State(TypedDict):
    input: str
    chat_history: Annotated[Sequence[BaseMessage], add_messages]
    context: str
    answer: str


system_prompt = """
Your name is SpaceDev.
Learn and interpret the code in the context, later you may be prompted to explain this code or recover it.
You will be used as a knowledge base, you are a helpful assistant that answer in the same language that you were asked the question.
Only use the sources provided in the context. Separated by four new lines, without saying they are sources, without wrapping in markdown code block, you will display the sources in a JSON format, containing the key "sources", it always being an array of strings, the strings will be the sources from the context you used to reach the response.

Example with sources (where <your_response /> is your own response):
<example_with_sources>
<your_response />

{{
  "sources": [
    "Wiki - How to make a RAG",
    "Wiki - How to index a document in a vector store"
  ]
}}
</example_with_sources>

<context>
{context}
</context>
"""

# """
# Answer the following question:
# {question}
# """


contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

vector_store = get_chroma()
retriever = vector_store.as_retriever()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

model = get_llm()


def format_docs(docs):
    context = ""

    for doc in docs:
        context += "Source: " + doc.metadata["source"]
        context += "\n\n"
        context += doc.page_content
        context += "\n\n"

    return context


history_aware_retriever = create_history_aware_retriever(
    model, retriever, contextualize_q_prompt
)

question_answer_chain = create_stuff_documents_chain(model, prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


def call_model(state: State):
    response = rag_chain.invoke(
        {
            "chat_history": state["chat_history"],
            "context": format_docs(state.get("context", [])),
            "input": state["input"],
            "answer": "",
        }
    )
    return {
        "chat_history": [
            HumanMessage(state["input"]),
            AIMessage(response["answer"]),
        ],
        "context": response["context"],
        "answer": response["answer"],
    }


workflow = StateGraph(State)

workflow.add_node("model", call_model)

workflow.add_edge(START, "model")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def get_chat_chain():
    return app
