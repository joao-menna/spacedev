from langchain.indexes import SQLRecordManager, index, IndexingResult
from langchain_core.documents import Document
from langchain_chroma import Chroma


def index_store(
    documents: list[Document],
    vector_store: Chroma,
    record_manager: SQLRecordManager,
    cleanup_mode: str,
) -> IndexingResult:
    return index(
        documents,
        record_manager,
        vector_store,
        cleanup=cleanup_mode,
        source_id_key="source",
    )
