import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path="app/.env")

BASE_USER_IMAGES_DIR = Path(os.getenv("BASE_USER_IMAGES_DIR"))
BASE_USER_IMAGES_DIR.mkdir(exist_ok=True) 

MOUNT_USER_IMAGES_PATH = os.getenv("MOUNT_USER_IMAGES_PATH")

IP = os.getenv("IP")