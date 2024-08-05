from fastapi import FastAPI
import uvicorn
from auth.router import auth_router
from posts.router import posts_router
from messages.router import messages_router
from starlette.middleware.cors import CORSMiddleware

# Инициализация приложения
app = FastAPI(
    title='Sinus Backend'
)



app.include_router(posts_router, tags=['Posts'])
app.include_router(auth_router, tags=['Authentification'])
app.include_router(messages_router, tags=['Messages'])

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)