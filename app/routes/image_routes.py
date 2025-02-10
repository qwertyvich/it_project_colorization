from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import uuid
from pathlib import Path
from app.services.image_service import save_image

router = APIRouter(prefix="/images", tags=["Images"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    filename = f"{uuid.uuid4()}.jpg"
    file_path = UPLOAD_DIR / filename
    save_image(file, file_path)

    return {"message": "Файл загружен", "file_path": str(file_path)}
