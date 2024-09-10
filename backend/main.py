import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
import uvicorn
import logging
from api.endpoints import generation_router

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Подключаем роутер для генерации
app.include_router(generation_router, prefix="/generation", tags=["Generation"])

# Подключаем шаблоны для веб-интерфейса
templates = Jinja2Templates(directory="backend/test/templates")

# Рендеринг главной страницы
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    logger.info("Запрос на главную страницу")
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())  # Явное указание использования asyncio loop
    uvicorn.run("app.main:app", reload=True)