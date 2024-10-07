from pydantic import BaseModel


class ChatInput(BaseModel):
    prompt: str
    chat_id: str
