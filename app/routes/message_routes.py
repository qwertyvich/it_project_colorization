from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/messages", tags=["Messages"])

class MessageRequest(BaseModel):
    message: str

@router.post("/process")
async def process_message(request: MessageRequest):
    #{"message": "тест"}
    # принимает сообщение и отправляет
    return {"received_message": request.message, "status": "processed"}
