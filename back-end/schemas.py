from pydantic import BaseModel

class UserMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
