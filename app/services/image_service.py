import shutil
from pathlib import Path
from fastapi import UploadFile

def save_image(file: UploadFile, path: Path):
    #сохранение файла
    with path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
