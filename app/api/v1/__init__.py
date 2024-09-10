from fastapi import APIRouter
from app.api.v1.endpoints import generation #, retrieval, evaluation

# Создание основного роутера для версии API v1
api_v1_router = APIRouter()

# Подключение маршрутов из отдельных модулей
api_v1_router.include_router(generation.router, prefix="/generation", tags=["generation"])
# api_v1_router.include_router(retrieval.router, prefix="/retrieval", tags=["retrieval"])
# api_v1_router.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])

