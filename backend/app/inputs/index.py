from pydantic import BaseModel

class Document(BaseModel):
    title: str
    content: str

class Path(BaseModel):
    path: str
    glob: str

class IndexInput(BaseModel):
    documents: list[Document] | None = None
    path: Path | None = None
