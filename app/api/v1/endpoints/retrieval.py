from fastapi import APIRouter, HTTPException
from app.milvus.milvus_utils import init_milvus, get_vector_store
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация Milvus при старте
init_milvus()

@router.post("/retrieve-context/")
async def retrieve_context(query: str):
    """
    Использование Milvus для поиска контекста по запросу.
    """
    try:
        logger.info(f"Поиск контекста для запроса: {query}")
        vector_store = get_vector_store()
        result = vector_store.similarity_search(query, k=5)
        return {"query": query, "context": result}
    except Exception as e:
        logger.error(f"Ошибка при поиске контекста: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка при поиске контекста")
