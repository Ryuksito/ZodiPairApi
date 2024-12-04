from pydantic import BaseModel, Field
from typing import Optional

class CreateChatModel(BaseModel):
    user_1_id: str
    user_2_id: str

class GetChatModel(BaseModel):
    id: int
    user_1_id: str
    user_2_id: str
    created_at: str
