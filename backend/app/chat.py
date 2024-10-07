from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from app.inputs.chat import ChatInput
from app.helpers.get_agent_chained import get_chat_chain

router = APIRouter()

@router.post("")
async def chat(chat_input: ChatInput):
    async def iter_response():
        chain = get_chat_chain()

        input_dict = {
            "input": chat_input.prompt,
        }

        # input_dict = {
        #     "messages": [
        #         ("system", system_prompt),
        #         ("human", chat_input.prompt),
        #     ],
        # }

        config = {
            "configurable": {
                "thread_id": chat_input.chat_id
            }
        }

        async for chunk in chain.astream(input_dict, config=config, stream_mode="messages"):
            print(chunk[0].content)
            yield chunk[0].content

        # async for chunk in chain.astream(input_dict, config=config, stream_mode="messages"):
        #     print(chunk[0].content)
        #     yield chunk[0].content

    try:
        headers = {"Cross-Origin-Allow-Origin": "*"}
        return StreamingResponse(iter_response(), media_type="text/plain", headers=headers)
    except Exception as e:
        print(e)
        return e
