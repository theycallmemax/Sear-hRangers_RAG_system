from fastapi import APIRouter
from app.services.retrieval import retrieve_context

router = APIRouter()

@router.post("/")
async def retrieve_context_api(query: str):
    """
    Эндпоинт для поиска контекста по запросу
    """
    context = retrieve_context(query)
    return {"context": context}
