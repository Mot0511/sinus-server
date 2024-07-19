from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from db.auth.auth import auth_backend
from db.auth.manager import get_user_manager
from db.auth.auth import auth_backend
from db.auth.schemas import UserCreate, UserRead, UserUpdate

auth_router = APIRouter(prefix='/auth')

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend]
)

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