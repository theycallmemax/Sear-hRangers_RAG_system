from fastapi import APIRouter, HTTPException
from logger import logger
from pydantic import BaseModel

from api.embeddings.make_request import make_request
from api.embeddings.milvus.create_collection import retriever

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
        answer, acts = make_request(query.question)

        logger.info(
            f"Ответ: '{answer}' успешно сгенерирован для вопроса: {query.question}"
        )
        return {"response": answer, "context": acts}

    except Exception as e:
        # Логируем и возвращаем ошибку с подробностями
        logger.error(
            f"Ошибка при генерации ответа: {str(e)}. Входные данные: {query.question}"
        )
        raise HTTPException(status_code=500, detail="Ошибка при генерации ответа")


# Создаем роутер
document_router = APIRouter()


# Модель данных для запроса
class DocumentInput(BaseModel):
    file_content: str


# Эндпоинт для добавления документа
@document_router.post("/add_document")
async def add_document(doc: DocumentInput):
    try:
        logger.info("Получен запрос на добавление документа.")
        
        if not doc.file_content:
            raise HTTPException(status_code=400, detail="Пустой файл")
        
        # Логирование данных перед вызовом retriever
        logger.info(f"Содержимое файла: {doc.file_content[:100]}")  # Логируем первые 100 символов

        # Возможно, функция retriever ожидает другой формат данных. Например, объект Document
        # Проверим, нужно ли обернуть текст в объект перед отправкой.
        # acts = [Document(content=doc.file_content)]
        acts = [doc.file_content]  # Просто передаём строку для отладки

        # Логируем перед добавлением
        logger.info(f"Перед добавлением в retriever: {acts}")

        # Добавление документа через retriever
        retriever.add_documents(acts)

        logger.info("Документ успешно добавлен в базу данных.")
        return {"message": "Документ успешно добавлен"}

    except Exception as e:
        logger.error(f"Ошибка при добавлении документа: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка добавления документа: {str(e)}")