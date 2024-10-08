from pydantic import BaseModel


class Document(BaseModel):
    title: str
    content: str


class Folder(BaseModel):
    path: str
    glob: str


class IndexInput(BaseModel):
    documents: list[Document] | None = None
    folders: list[Folder] | None = None
