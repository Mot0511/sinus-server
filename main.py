from fastapi import FastAPI
from auth.router import auth_router
from posts.router import posts_router
from starlette.middleware.cors import CORSMiddleware

# Инициализация приложения
app = FastAPI(
    title='Sinus Backend'
)



app.include_router(posts_router, tags=['Posts'])
app.include_router(auth_router)

@app.get('/')
def start():
    return 'Server is working'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)