from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints import retrieval, generation, evaluation
from pydantic import BaseModel

print('*')
app = FastAPI()

# Подключаем папку с шаблонами (HTML-файлами) и статическими файлами
templates = Jinja2Templates(directory="frontend/pages")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Подключаем маршруты
app.include_router(retrieval.router, prefix="/api/v1/retrieval", tags=["retrieval"])
app.include_router(generation.router, prefix="/api/v1/generation", tags=["generation"])
app.include_router(evaluation.router, prefix="/api/v1/evaluation", tags=["evaluation"])

# Класс для обработки входящих сообщений
class Message(BaseModel):
    message: str

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Эндпоинт для обработки сообщений
@app.post("/submit_message")
def submit_message(message: Message):
    response_message = 'Ответ на сообщение.'
    return {"user_message": message.message, "response_message": response_message}
