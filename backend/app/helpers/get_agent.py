from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_core.documents import Document
from langgraph.graph import START, END, StateGraph
from typing_extensions import Annotated, TypedDict
from typing import Sequence
import operator
import json

from app.helpers.get_chroma import get_chroma
from app.helpers.get_llm import get_llm, get_llm_json

generation_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template="""
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
    "Wiki - How to index a document in a vector store"
  ]
}}
</example_with_sources>

<context>
{context}
</context>

Answer the following question:

{question}
""",
)

retrieval_grader_prompt = PromptTemplate(
    input_variables=["question", "document"],
    template="""
You are a grader assessing relevance of a retrieved document to a user question. \n 
Here is the retrieved document: \n\n {document} \n\n
Here is the user question: {question} \n
If the document contains keywords related to the user question, grade it as relevant. \n
It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
Provide the binary score as a JSON with a single key 'score' and no premable or explanation.
""",
)

hallucination_grader_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template="""
You are a grader assessing whether an answer is grounded in / supported by a set of facts. \n 
Here are the facts:
\n ------- \n
{documents} 
\n ------- \n
Here is the answer: {generation}
Give a binary score 'yes' or 'no' score to indicate whether the answer is grounded in / supported by a set of facts. \n
Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
""",
)

answer_grader_prompt = PromptTemplate(
    input_variables=["generation", "question"],
    template="""
You are a grader assessing whether an answer is useful to resolve a question. \n 
Here is the answer:
\n ------- \n
{generation} 
\n ------- \n
Here is the question: {question}
Give a binary score 'yes' or 'no' to indicate whether the answer is useful to resolve a question. \n
Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
""",
)

question_rewriter_prompt = PromptTemplate(
    input_variables=[],
    template="""
You a question re-writer that converts an input question to a better version that is optimized \n 
for vectorstore retrieval. Look at the initial and formulate an improved question. \n
Here is the initial question: \n\n {question}. Improved question with no preamble: \n 
""",
)

llm = get_llm()
llm_json_mode = get_llm_json()

generation = generation_prompt | llm | StrOutputParser()
retrieval_grader = retrieval_grader_prompt | llm_json_mode | JsonOutputParser()
hallucination_grader = hallucination_grader_prompt | llm_json_mode | JsonOutputParser()
answer_grader = answer_grader_prompt | llm_json_mode | JsonOutputParser()
question_rewriter = question_rewriter_prompt | llm | StrOutputParser()


class GraphState(TypedDict):
    question: str
    generation: str
    documents: list[str]


def format_docs(docs):
    context = ""

    for doc in docs:
        context += "Source: " + doc.metadata["source"]
        context += "\n\n"
        context += doc.page_content
        context += "\n\n---\n\n"

    return context


def retrieve(state: GraphState):
    print("Retrieving...")

    question = state["question"]

    vector_store = get_chroma()
    retriever = vector_store.as_retriever()

    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}


def generate(state: GraphState):
    print("Generating...")

    question = state["question"]
    documents = state["documents"]

    docs_txt = format_docs(documents)

    llm = get_llm()
    generation_result = generation.invoke({"context": documents, "question": question})

    return {
        "generation": generation_result,
        "question": question,
        "documents": documents,
    }


def grade_documents(state: GraphState):
    print("Filtering documents...")

    question = state["question"]
    documents = state["documents"]

    filtered_docs = []

    for doc in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": doc.page_content}
        )

        grade = score["score"]

        if grade.lower() == "yes":
            filtered_docs.append(doc)

    return {"documents": filtered_docs, "question": question}


def transform_query(state: GraphState):
    print("Regenerating question")

    question = state["question"]
    documents = state["documents"]

    better_question = question_rewriter.invoke({"question": question})

    return {"documents": documents, "question": better_question}


def decide_to_generate(state: GraphState):
    question = state["question"]
    filtered_docs = state["documents"]

    if not filtered_docs:
        return "transform_query"

    return "generate"


def grade_generation_v_documents_and_question(state):
    print("Checking Hallucinations...")

    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    grade = score["score"]

    if grade == "yes":
        score = answer_grader.invoke({"question": question, "generation": generation})
        grade = score["score"]

        if grade == "yes":
            return "useful"
        else:
            return "not useful"
    else:
        return "not supported"


workflow = StateGraph(state_schema=GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("transform_query", transform_query)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "retrieve")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "transform_query",
    },
)

memory = MemorySaver()

app = workflow.compile(checkpointer=memory)


def get_chat_chain():
    return app
