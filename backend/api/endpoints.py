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

from langchain.schema import Document  # Исправлено имя класса

# Эндпоинт для добавления документа
@document_router.post("/add_document")
async def add_document(doc: DocumentInput):
    try:
        if not doc.file_content:
            raise HTTPException(status_code=400, detail="Пустой файл")
        
        # Разделяем содержимое файла на строки и создаём объекты Document
        acts = doc.file_content.split("\n")[0:10]  # Берём первые 10 строк
        documents = [Document(page_content=act) for act in acts if act]  # Создаём объекты Document

        # Добавление документов через retriever
        retriever.add_documents(documents)
        return {"message": "Документ успешно добавлен"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка добавления документа: {str(e)}")
