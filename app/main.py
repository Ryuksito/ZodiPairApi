
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import BASE_USER_IMAGES_DIR, MOUNT_USER_IMAGES_PATH
from app.api.routes import users_images, user, user_request

app = FastAPI()

app.include_router(users_images.router)
app.include_router(user.router)
app.include_router(user_request.router)

# Monta el directorio de imágenes como un recurso estático
app.mount(MOUNT_USER_IMAGES_PATH, StaticFiles(directory=BASE_USER_IMAGES_DIR), name="users")

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}