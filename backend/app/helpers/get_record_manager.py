from langchain.indexes import SQLRecordManager

def get_record_manager() -> SQLRecordManager:
    record_manager = SQLRecordManager(
        namespace="chromadb/spacedev",
        db_url="file:record_manager_cache.db"
    )

    record_manager.create_schema()

    return record_manager
