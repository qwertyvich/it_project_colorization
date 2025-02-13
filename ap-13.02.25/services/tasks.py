# app/services/tasks.py

import io
import os
import uuid
from celery import Celery
from PIL import Image, ImageOps

BROKER_URL = "amqp://guest:guest@localhost:5672//"
BACKEND_URL = "rpc://"  # или "redis://..."

celery_app = Celery("tasks", broker=BROKER_URL, backend=BACKEND_URL)

# Папка, куда складываем обработанные файлы.
# Убедитесь, что она существует (или используйте os.makedirs).
PROCESSED_FOLDER = os.path.join("app", "static", "processed")
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@celery_app.task
def process_image_task(image_bytes: bytes) -> str:
    """
    Примитивная заглушка. Инвертируем цвета и сохраняем
    PNG-файл на диск. Возвращаем путь к сохранённому файлу.
    """
    with Image.open(io.BytesIO(image_bytes)) as img:
        inverted_img = ImageOps.invert(img.convert("RGB"))

        # Генерируем уникальное имя файла, чтобы не перезаписывать старые
        filename = f"{uuid.uuid4().hex}.png"
        file_path = os.path.join(PROCESSED_FOLDER, filename)

        # Сохраняем изображение на диск
        inverted_img.save(file_path, format="PNG")

        # Возвращаем путь к файлу (строкой)
        return file_path

