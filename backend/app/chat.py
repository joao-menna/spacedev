from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.inputs.chat import ChatInput
from app.helpers.get_chat_chain import get_chat_chain

router = APIRouter()

@router.post("")
def chat(chat_input: ChatInput):
    def iter_response():
        chain = get_chat_chain()

        for chunk in chain.stream(chat_input.prompt):
            print(chunk)
            yield chunk

    try:
        headers = {"Cross-Origin-Allow-Origin": "*"}
        return StreamingResponse(iter_response(), media_type="text/plain", headers=headers)
    except Exception as e:
        print(e)
        return e
