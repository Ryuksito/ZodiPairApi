from pydantic import BaseModel, Field
from typing import Optional

class CreateMessageModel(BaseModel):
    chat_id: int
    sender_id: str
    content: str
    status: str = Field(..., pattern="^(sended|received)$")

class GetMessageModel(BaseModel):
    id: int
    chat_id: int
    sender_id: str
    content: str
    status: str
    created_at: str
