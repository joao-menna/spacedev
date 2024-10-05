from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.inputs.chat import ChatInput
from app.helpers.get_llm import get_llm

router = APIRouter()

@router.post("")
async def chat(chat_input: ChatInput):
    async def iter_response():
        model = get_llm()

        messages = [
            ("system", "You are a helpful translator. Translate the user sentence to French."),
            ("human", chat_input.prompt),
        ]

        async for chunk in model.astream(messages):
            yield chunk.content

    return StreamingResponse(iter_response(), media_type="text/plain")
