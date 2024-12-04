import random
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from app.config import BASE_USER_IMAGES_DIR, IP, MOUNT_USER_IMAGES_PATH
from app.services import ZodiPairDB
from app.models import GetRandomUsersModel, GetUserModel, GetProfileModel, UserListModel, UserValidationModel

router = APIRouter(prefix="/users", tags=["Users"])

db = ZodiPairDB()

@router.post("/user-validation")
async def post_user_validation(user_validation: UserValidationModel):
    print("User validation: ", user_validation)
    get_user: GetUserModel = db.get_user(user_validation)

    return get_user

@router.post("/get-profile")
async def post_user_validation(user_id: str):
    print("user_id: ", user_id)
    get_profile: GetProfileModel = db.get_profile(user_id)

    return get_profile