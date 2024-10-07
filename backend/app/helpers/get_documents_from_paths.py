from langchain_community.document_loaders import DirectoryLoader, TextLoader
from app.inputs.index import Folder


def get_documents_from_paths(folders: list[Folder]):
    docs = []

    text_loader_kwargs = {"autodetect_encoding": True}

    for folder in folders:
        loader = DirectoryLoader(
            folder.path,
            glob=folder.glob,
            loader_cls=TextLoader,
            show_progress=True,
            use_multithreading=True,
            loader_kwargs=text_loader_kwargs,
        )

        for doc in loader.load():
            docs.append(doc)

    return docs
