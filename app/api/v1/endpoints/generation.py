import logging
from fastapi import APIRouter, HTTPException
from llama.llama_model import generate_with_llama
from pydantic import BaseModel

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Query(BaseModel):
    question: str


@router.post("/")
async def generate_answer_api(query : Query):
    """
    Генерация ответа на вопрос.
    """
    try:
        logger.info(f"Запрос на генерацию ответа для вопроса: { query.question }")
        answer = generate_with_llama(query.question)
        logger.info(f"Ответ: '{answer}' успешно сгенерирован для вопроса: {query.question}")
        return {"question": query.question, "answer": answer}
    except Exception as e:
        logger.error(f"Ошибка при генерации ответа: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка при генерации ответа")
