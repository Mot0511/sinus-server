from fastapi import APIRouter, Form, UploadFile
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.auth import auth_backend
from auth.schemas import UserCreate, UserRead, UserUpdate
from fastapi.responses import FileResponse

auth_router = APIRouter(prefix='/auth')

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend]
)

@auth_router.get('/getAvatar/{id}')
def getAvatar(id: str):
    return FileResponse(f'storage/avatars/{id}.png')

@auth_router.post('/setAvatar')
def setAvatar(avatar: UploadFile, id: str = Form()):
    print(avatar)
    print(id)
    with open(f'storage/avatars/{id}.png', 'wb') as file:
        file.write(avatar.file.read())

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='',
    tags=['Authentification']
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='',
    tags=['Authentification']
)

auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='',
    tags=['Authentification']
)

auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='',
    tags=['Authentification']
)
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='',
    tags=["Authentification"],
)