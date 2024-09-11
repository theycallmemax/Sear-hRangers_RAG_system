from api.embeddings.make_request import make_request
from fastapi import APIRouter, HTTPException
from logger import logger
from pydantic import BaseModel

# Создаем роутер для генерации ответов
generation_router = APIRouter()


# Определяем модель запроса
class Query(BaseModel):
    question: str


# Определяем эндпоинт для генерации ответа
@generation_router.post("/")
async def generate_answer_api(query: Query):
    """
    Генерация ответа на вопрос.

    Этот эндпоинт принимает запрос с вопросом и возвращает сгенерированный ответ,
    основанный на контексте, извлеченном из базы данных.
    """
    try:
        logger.info(f"Запрос на генерацию ответа для вопроса: { query.question }")

        # Генерация ответа с использованием make_request
        answer = make_request(query.question)

        logger.info(
            f"Ответ: '{answer}' успешно сгенерирован для вопроса: {query.question}"
        )

        return {"question": query.question, "answer": answer}

    except Exception as e:
        # Логируем и возвращаем ошибку с подробностями
        logger.error(
            f"Ошибка при генерации ответа: {str(e)}. Входные данные: {query.question}"
        )
        raise HTTPException(status_code=500, detail="Ошибка при генерации ответа")
