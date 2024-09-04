from fastapi import FastAPI
from app.api.v1.endpoints import retrieval, generation, evaluation

app = FastAPI()

# Подключаем маршруты
app.include_router(retrieval.router, prefix="/api/v1/retrieval", tags=["retrieval"])
app.include_router(generation.router, prefix="/api/v1/generation", tags=["generation"])
app.include_router(evaluation.router, prefix="/api/v1/evaluation", tags=["evaluation"])

@app.get("/")
def read_root():
    return {"message": "Привет"}
