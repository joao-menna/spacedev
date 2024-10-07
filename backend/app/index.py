from fastapi import APIRouter
from langchain_core.documents import Document
from app.inputs.index import IndexInput
from app.helpers.get_documents_from_paths import get_documents_from_paths
from app.helpers.get_embedding_model import get_embedding_model
from app.helpers.get_record_manager import get_record_manager
from app.helpers.index_store import index_store
from app.helpers.get_chroma import get_chroma
import shutil
import os

router = APIRouter()


@router.post("/everything")
async def index_all(body: IndexInput):
    vector_store = get_chroma()
    record_manager = get_record_manager()

    try:
        docs_from_paths = []
        docs_from_text = []

        if not body.folders is None:
            docs_from_paths = get_documents_from_paths(body.folders)

        if not body.documents is None:
            for doc in body.documents:
                docs_from_text.append(
                    Document(page_content=doc.content, metadata={"source": doc.title})
                )

        all_docs = docs_from_paths + docs_from_text

        result = index_store(all_docs, vector_store, record_manager, "incremental")

        return {"success": True, "result": result}
    except Exception as e:
        print(e)
        return {"success": False}


@router.post("")
async def index_one(body: IndexInput):
    vector_store = get_chroma()
    record_manager = get_record_manager()

    try:
        docs_from_paths = []
        docs_from_text = []

        if not body.paths is None:
            docs_from_paths = get_documents_from_paths(body.paths)

        if not body.documents is None:
            for doc in body.documents:
                docs_from_text.append(
                    Document(page_content=doc.content, metadata={"source": doc.title})
                )

        all_docs = docs_from_paths + docs_from_text

        result = index_store(all_docs, vector_store, record_manager, "incremental")
        # ids = vector_store.add_documents(all_docs)

        return {"success": True, "result": result}
    except:
        return {"success": False}


@router.delete("")
async def index_clear():
    directory = os.path.abspath(os.path.join(os.getcwd(), "chroma"))

    shutil.rmtree(directory)

    return {"success": True}
