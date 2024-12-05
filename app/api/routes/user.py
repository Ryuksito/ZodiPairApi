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
    get_user: GetUserModel = db.get_user(user_validation)

    return get_user

@router.post("/get-profile")
async def post_user_validation(user_id: str):
    get_profile: GetProfileModel = db.get_profile(user_id)

    get_profile.img = f"http://{IP}{MOUNT_USER_IMAGES_PATH}/{get_profile.img}"
    get_profile.imgs = [f"http://{IP}{MOUNT_USER_IMAGES_PATH}/{img}" for img in get_profile.imgs]

    print(get_profile)

    return get_profile

@router.get("/user", response_model=GetUserModel)
async def get_user(user_id: str):
    """
    Endpoint para obtener un usuario por su ID.

    :param user_id: El ID del usuario a buscar.
    :return: Un modelo `GetUserModel` con los datos del usuario.
    """
    response = db.find_user(user_id)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response