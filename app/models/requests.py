from pydantic import BaseModel, Field
from typing import Optional

class CreateRequestModel(BaseModel):
    hearts: list[str] = []
    hot_hearts: list[str] = []

class GetRequestModel(BaseModel):
    id: int
    hearts: list[str]
    hot_hearts: list[str]

class GetUserRequestModel(BaseModel):
    user_id: str  

class UpdateRequestModel(BaseModel):
    user_id: str  
    sender_id: str  
    is_hot_love: bool 

class UpdateRequestResponseModel(BaseModel):
    status: bool
