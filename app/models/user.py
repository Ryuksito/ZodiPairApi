from pydantic import BaseModel, Field
from typing import Optional


class CreateUserModel(BaseModel):
    user_name: str
    password: str
    profile_id: int
    requests_id: Optional[int] = None

class GetUserModel(BaseModel):
    id: str
    user_name: str
    profile_id: int
    requests_id: Optional[int] = None

class UserListModel(BaseModel):
    users: list[GetUserModel]

class UserValidationModel(BaseModel):
    user_name: str
    password: str

class GetRandomUsersModel(BaseModel):
    count: int
    id: str