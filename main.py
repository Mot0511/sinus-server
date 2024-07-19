from fastapi import FastAPI
from db.auth.router import auth_router
from starlette.middleware.cors import CORSMiddleware

# Инициализация приложения
app = FastAPI(
    title='Sinus Backend'
)

@app.get('/')
def start():
    return 'Server is working'

app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)