from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.inputs.chat import ChatInput
from app.helpers.get_chat_chain import get_chat_chain

router = APIRouter()

@router.post("")
async def chat(chat_input: ChatInput):
    async def iter_response():
        chain = get_chat_chain()

        async for chunk in chain.astream(chat_input.prompt):
            print(chunk)
            yield chunk

    try:
        return StreamingResponse(iter_response(), media_type="text/plain")
    except:
        return False
