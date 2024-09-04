from fastapi import APIRouter
from app.services.evaluation import evaluate_answer

router = APIRouter()

@router.post("/")
async def evaluate_answer_api(answer: str, context: str):
    """
    Эндпоинт для оценки качества ответа
    """
    score = evaluate_answer(answer, context)
    return {"evaluation_score": score}
