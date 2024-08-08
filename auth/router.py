from os import access
from fastapi import APIRouter, Form, UploadFile, Depends
import fastapi_users
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.auth import auth_backend
from auth.schemas import UserCreate, UserRead, UserUpdate
from fastapi.responses import FileResponse
from db.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from db.models import User
from schemas import UsersPair
import json


auth_router = APIRouter(prefix='/auth')

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user()

# Need to auth
@auth_router.post('/friends/{action}/{id}')
async def friendsAction(id: str, action: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    q = select(User.friends).where(User.id == user.id)
    data = await session.execute(q)
    friends = json.loads(data.scalar())
    if action == 'add':
        friends.append(id)
    elif action == 'remove':
        friends.remove(id)
    q = update(User).where(User.id == user.id).values(
        friends = json.dumps(friends)
    )
    await session.execute(q)
    await session.commit()


@auth_router.get('/getFriends/{id}')
async def getFriends(id: str, session: AsyncSession = Depends(get_async_session)):
    q = select(User.friends).where(User.id == id)
    data = await session.execute(q)
    friends_ids = json.loads(data.scalar())

    friends = []
    for friend_id in friends_ids:
        q = select(User).where(User.id == friend_id)
        data = await session.execute(q)
        friends.append(data.scalar())

    return friends


@auth_router.get('/getAvatar/{id}')
def getAvatar(id: str):
    return FileResponse(f'storage/avatars/{id}.png')

# Need to auth
@auth_router.post('/setAvatar')
def setAvatar(avatar: UploadFile, user: User = Depends(current_user)):
    with open(f'storage/avatars/{user.id}.png', 'wb') as file:
        file.write(avatar.file.read())

@auth_router.get('/getUsers')
async def getUsers(session: AsyncSession = Depends(get_async_session)):
    q = select(User)
    data = await session.execute(q)
    users = data.scalars().all()
    
    return users

@auth_router.get('/getUser/{id}')
async def getUser(id: str, session: AsyncSession = Depends(get_async_session)):
    q = select(User).where(User.id == id)
    data = await session.execute(q)
    user = data.scalar()

    return user

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='',
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='',
)

auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='',
)

auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='',
)
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='',
)