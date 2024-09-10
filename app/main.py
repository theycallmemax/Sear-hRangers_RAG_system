from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Подключаем папку с шаблонами (HTML-файлами) и статическими файлами
templates = Jinja2Templates(directory="frontend/templates")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Класс для обработки входящих сообщений
class Message(BaseModel):
    message: str

class SourceRequest(BaseModel):
    source_name: str

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Эндпоинт для обработки сообщений
@app.post("/submit_message")
def submit_message(message: Message):
    response_message = 'Ответ на вопрос'
    sources = ['НПА 1', 'НПА 2']
    return {"user_message": message.message, "response_message": response_message, "sources": sources}

# Эндпоинт для получения контента источника
@app.post("/get_source_content")
def get_source_content(source_request: SourceRequest):
    # Заглушка для контента источника, позже можно подключить БД
    source_content = 'Текст выделенного НПА'
    return {"source_content": source_content}
