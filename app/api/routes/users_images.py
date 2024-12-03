import random
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.config import BASE_USER_IMAGES_DIR, IP, MOUNT_USER_IMAGES_PATH

router = APIRouter(prefix="/users/images", tags=["Images"])

@router.get("/random/{count}")
async def get_random_user_images(count: int):
    """
    Devuelve una lista aleatoria de imágenes de perfil en formato .jpg de todos los usuarios.
    """
    if not BASE_USER_IMAGES_DIR.exists() or not BASE_USER_IMAGES_DIR.is_dir():
        raise HTTPException(status_code=404, detail="Image directory not found")

    # Buscar todas las carpetas con el prefijo "user_"
    user_dirs = [d for d in BASE_USER_IMAGES_DIR.iterdir() if d.is_dir()]
    
    if not user_dirs:
        raise HTTPException(status_code=404, detail="No user directories found")
    
    profile_images = []
    for user_dir in user_dirs:
        # Buscar todas las imágenes .jpg dentro de la carpeta del usuario
        image_files = [img for img in user_dir.iterdir() if img.suffix.lower() == ".jpg"]
        profile_images.extend(image_files)

    if not profile_images:
        raise HTTPException(status_code=404, detail="No profile images found")
    
    # Seleccionar imágenes aleatorias
    random_images = random.sample(profile_images, min(count, len(profile_images)))

    # Construir la respuesta con las URLs y las imágenes seleccionadas
    return [
        {"filename": img.name, 
         "user_id": img.parent.name, 
         "url": f"http://{IP}{MOUNT_USER_IMAGES_PATH}/{img.parent.name}/{img.name}"
        } for img in random_images
    ]
