# app/routes/image_routes.py

import io
from fastapi import Request
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.services.tasks import process_image_task
from app.services.tasks import BROKER_URL, BACKEND_URL

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()
@router.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Принимаем файл, ставим задачу Celery и возвращаем ID задачи.
    """
    image_bytes = await file.read()
    task = process_image_task.delay(image_bytes)
    return JSONResponse(content={
        "task_id": task.id,
        "result_url": f"/result/{task.id}"
    })

@router.get("/result/{task_id}")
def get_result(task_id: str):
    """
    Проверяем состояние задачи. Если готово — отдаём картинку.
    Если нет — возвращаем сообщение, что в процессе.
    """
    task_result = process_image_task.AsyncResult(task_id)

    if not task_result.ready():
        print("BROKER_URL=", BROKER_URL, "BACKEND_URL=", BACKEND_URL)  # или celery_app.conf
        print("task status:", task_result.status)
        return JSONResponse(content={"status": "Processing..."})

    if task_result.failed():
        raise HTTPException(status_code=500, detail="Ошибка в задаче Celery")

    processed_bytes = task_result.get()

    # Возвращаем изображение в потоке
    return StreamingResponse(
        io.BytesIO(processed_bytes), 
        media_type="image/png",
        headers={
            "Content-Disposition": "attachment; filename=result.png"
        }
    )

