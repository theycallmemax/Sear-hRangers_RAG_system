from dotenv import load_dotenv

load_dotenv()
import asyncio

import uvicorn
from api.endpoints import generation_router
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from logger import logger

app = FastAPI()

# Подключаем роутер для генерации
app.include_router(generation_router, prefix="/generation", tags=["Generation"])

# Подключаем шаблоны для веб-интерфейса
templates = Jinja2Templates(directory="test/templates")
app.mount("/static", StaticFiles(directory="test/static"), name="static")


# Рендеринг главной страницы
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    logger.info("Запрос на главную страницу")
    return templates.TemplateResponse("index.html", {"request": request})



if __name__ == "__main__":
    asyncio.set_event_loop_policy(
        asyncio.DefaultEventLoopPolicy()
    )  # Явное указание использования asyncio loop
    uvicorn.run("app.main:app", reload=True)

