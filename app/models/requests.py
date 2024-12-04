from pydantic import BaseModel, Field
from typing import Optional

class CreateRequestModel(BaseModel):
    hearts: list[str] = []
    hot_hearts: list[str] = []

class GetRequestModel(BaseModel):
    id: int
    hearts: list[str]
    hot_hearts: list[str]
