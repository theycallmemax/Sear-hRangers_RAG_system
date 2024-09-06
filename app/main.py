import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.v1 import api_v1_router
import asyncio
import uvicorn

app = FastAPI()

app.include_router(api_v1_router, prefix="/api/v1")

# Подключаем шаблоны для веб-интерфейса
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())  # Явное указание использования asyncio loop
    uvicorn.run("app.main:app", reload=True)
