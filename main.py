import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
from auth.router import auth_router
from config import DB_URI
from db.models import Base
from db.db import create_db, drop_db
from posts.router import posts_router
from messages.router import messages_router
from starlette.middleware.cors import CORSMiddleware
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Lifespan')
    await create_db()
    yield

# Инициализация приложения
app = FastAPI(
    title='Sinus Backend',
    lifespan=lifespan
)

app.include_router(posts_router, tags=['Posts'])
app.include_router(auth_router, tags=['Authentification'])
app.include_router(messages_router, tags=['Messages'])

@app.get('/')
def start():
    return 'Server is working'

@app.get('/create_db')
async def create_db_route():
    await create_db()

@app.get('/drop_db')
async def create_db_route():
    await drop_db()

@app.get('/getlogs')
def get_logs():
    return FileResponse('logs.txt')

@app.get('/set_logging')
def set_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("logs.txt")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'https://pipeup.vercel.app'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
