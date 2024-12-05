import random
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from app.config import BASE_USER_IMAGES_DIR, IP, MOUNT_USER_IMAGES_PATH
from app.services import ZodiPairDB
from app.models import UpdateRequestModel, UpdateRequestResponseModel

router = APIRouter(prefix="/users/requests", tags=["Users"])

db = ZodiPairDB()

@router.put("/add")
async def add_user_request(updateRequestModel: UpdateRequestModel):
    response: UpdateRequestResponseModel = db.add_request(updateRequestModel)

    return response