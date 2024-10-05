from fastapi import APIRouter
from app.inputs.index import IndexInput

router = APIRouter()

@router.post("everything")
async def index_all(body: IndexInput):
    pass

@router.post("")
async def index_one(body: IndexInput):
    pass

@router.delete("")
async def index_clear():
    pass
