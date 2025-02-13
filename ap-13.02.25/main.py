# app/main.py

from fastapi import FastAPI
from app.routes.image_routes import router as image_router

def create_app() -> FastAPI:
    """
    Функция для создания приложения,
    чтобы в будущем при необходимости передавать настройки.
    """
    app = FastAPI(title="Colorizer Project")
    app.include_router(image_router)
    return app

app = create_app()

# Если хотите использовать Jinja2Templates, можно сделать так:
# from fastapi.templating import Jinja2Templates
# templates = Jinja2Templates(directory="app/templates")
#
# И в роутах, где нужен шаблон, передавать:
# return templates.TemplateResponse("index.html", {"request": request})
