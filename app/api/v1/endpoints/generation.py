from fastapi import APIRouter
from app.services.generation import generate_answer

router = APIRouter()

@router.post("/")
async def generate_answer_api(context: str):
    """
    Эндпоинт для генерации ответа на основе контекста
    """
    answer = generate_answer(context)
    return {"answer": answer}
