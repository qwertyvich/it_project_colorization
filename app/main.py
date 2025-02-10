from fastapi import FastAPI
from app.routes.image_routes import router as image_router
from app.routes.health import router as health_router
from app.routes.message_routes import router as message_router

app = FastAPI(
    title="Server",
    description="maket",
    version="1.0"
)

app.include_router(image_router)
app.include_router(health_router)
app.include_router(message_router)

@app.get("/")
def root():
    return {"message": "Сервер работает!"}
