import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path="app/.env")

BASE_USER_IMAGES_DIR = Path(os.getenv("BASE_USER_IMAGES_DIR"))
BASE_USER_IMAGES_DIR.mkdir(exist_ok=True) 

MOUNT_USER_IMAGES_PATH = os.getenv("MOUNT_USER_IMAGES_PATH")

IP = os.getenv("IP")

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
