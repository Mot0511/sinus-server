from fastapi import APIRouter, Form, UploadFile, Depends
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.auth import auth_backend
from auth.schemas import UserCreate, UserRead, UserUpdate
from fastapi.responses import FileResponse
from db.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from auth.models import User
from auth.schemas import FriendsAction
import json


auth_router = APIRouter(prefix='/auth')

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend]
)

@auth_router.post('/friends/{action}')
async def friendsAction(ids: FriendsAction, action: str, session: AsyncSession = Depends(get_async_session)):
    q = select(User.friends).where(User.id == ids.user1)
    data = await session.execute(q)
    friends = json.loads(data.scalar())
    if action == 'add':
        friends.append(ids.user2)
    elif action == 'remove':
        friends.remove(ids.user2)
    q = update(User).where(User.id == ids.user1).values(
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

@auth_router.post('/setAvatar')
def setAvatar(avatar: UploadFile, id: str = Form()):
    print(avatar)
    print(id)
    with open(f'storage/avatars/{id}.png', 'wb') as file:
        file.write(avatar.file.read())

@auth_router.get('/getUsers')
async def getUsers(session: AsyncSession = Depends(get_async_session)):
    q = select(User)
    data = await session.execute(q)
    users = data.scalars().all()
    
    return users

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