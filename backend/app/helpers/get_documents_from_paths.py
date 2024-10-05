from langchain_community.document_loaders import DirectoryLoader
from app.inputs.index import Folder

def get_documents_from_paths(folders: list[Folder]):
    docs = []

    for folder in folders:
        loader = DirectoryLoader(folder.path, glob=folder.glob, show_progress=True)
        for doc in loader.load():
            docs.append(doc)

    return docs
