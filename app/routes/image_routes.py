import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.tasks import process_image_task, PROCESSED_FOLDER

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def index_page():
    """
    Простейшая HTML-форма загрузки.
    """
    return """
    <html>
      <head><title>Загрузка изображения</title></head>
      <body>
        <h1>Загрузите изображение</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
          <input type="file" name="file" accept="image/*" required/>
          <button type="submit">Загрузить</button>
        </form>
      </body>
    </html>
    """

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    1) Принимаем картинку
    2) Синхронно вызываем Celery-задачу (task.get()) -- блокирующий вызов
    3) Редиректим на страницу /show/{filename}, где картинка будет видна
    """
    image_bytes = await file.read()

    # --- Внимание: блокирующий вызов ---
    # Вместо .delay(...) + опроса, вызываем .apply(...) и get()
    # Это дождётся конца обработки!
    result_async = process_image_task.apply(args=[image_bytes])
    file_path = result_async.get()  # дождались конца Celery-задачи

    # Возвращается полный путь (app/static/processed/abc123.png)
    filename = os.path.basename(file_path)

    # Перенаправляем на эндпойнт /show/{filename}
    return RedirectResponse(url=f"/show/{filename}", status_code=302)

@router.get("/show/{filename}", response_class=HTMLResponse)
def show_processed_image(filename: str):
    """
    Показываем страницу с готовым изображением,
    которое лежит в /static/processed/{filename}.
    """
    # Проверим, что файл реально есть
    full_path = os.path.join(PROCESSED_FOLDER, filename)
    if not os.path.exists(full_path):
        raise HTTPException(404, detail="Файл не найден")

    # Вернём простой HTML с <img> на него:
    return f"""
    <html>
      <head><title>Результат обработки</title></head>
      <body>
        <h1>Готовая картинка</h1>
        <img src="/static/processed/{filename}" alt="результат">
      </body>
    </html>
    """
