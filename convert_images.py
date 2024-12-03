import uuid
from pathlib import Path
from PIL import Image
import os

# Ruta base de las carpetas de usuarios
BASE_DIR = Path("app/images/users")

def convert_to_jpg():
    """
    Recorre las carpetas de usuarios y convierte imágenes de otros formatos a .jpg.
    Soporta archivos .webp, .png, .avif, etc.
    """
    for user_dir in BASE_DIR.glob("user_*"):
        if user_dir.is_dir():
            print(f"Procesando carpeta: {user_dir.name}")
            
            for image_file in user_dir.iterdir():
                if image_file.suffix.lower() not in [".jpg"]:  # Filtra imágenes que no son .jpg
                    try:
                        # Abre la imagen y la convierte a RGB (necesario para JPG)
                        with Image.open(image_file) as img:
                            img = img.convert("RGB")
                            
                            # Generar un nombre único para la nueva imagen
                            unique_filename = f"{image_file.stem}_{uuid.uuid4().hex}.jpg"
                            new_file = user_dir / unique_filename
                            
                            # Guarda la nueva imagen en formato JPG
                            img.save(new_file, "JPEG")
                            print(f"Convertido: {image_file.name} -> {new_file.name}")
                        
                        # Elimina el archivo original después de la conversión
                        image_file.unlink()
                    
                    except Exception as e:
                        print(f"Error procesando {image_file.name}: {e}")

if __name__ == "__main__":
    convert_to_jpg()
