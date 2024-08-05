from fastapi import APIRouter, Depends, UploadFile, Form, File, Request
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from posts.schemas import Post
from db.models import Post as PostModel
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
import random

posts_router = APIRouter(prefix='/posts')

# Need to auth
@posts_router.post('/add')
async def addPost(image: UploadFile, user = Form(), text = Form(), session: AsyncSession = Depends(get_async_session)):
    id = random.randint(1, 1000000)
    
    obj = PostModel(
        id = id,
        user = user,
        text = text
    )
    session.add(obj)
    await session.commit()

    with open(f'storage/posts/{id}.png', 'wb') as file:
        file.write(image.file.read())

    return ''


@posts_router.get('/getOne/{id}')
async def getPost(id: int, session: AsyncSession = Depends(get_async_session)):
    q = select(PostModel).where(PostModel.id == id)
    data = await session.execute(q)
    post = data.scalar()

    return post

@posts_router.get('/get/{userID}')
async def getPosts(userID: str, session: AsyncSession = Depends(get_async_session)):
    q = select(PostModel).where(PostModel.user == userID)
    data = await session.execute(q)
    posts = data.scalars().all()

    return posts

@posts_router.get('/get')
async def getAllPosts(session: AsyncSession = Depends(get_async_session)):
    q = select(PostModel)
    data = await session.execute(q)
    posts = data.scalars().all()

    return posts

@posts_router.get('/getImage/{id}')
async def getPostImage(id: str):
    return FileResponse(path=f'storage/posts/{id}.png')

# Need to auth
@posts_router.put('/edit/{id}')
async def editPost(image: UploadFile, user = Form(), text = Form(), session: AsyncSession = Depends(get_async_session)):
    
    q = update(PostModel).where(PostModel.id == id).values(
        text = text
    )
    session.execute(q)
    await session.commit()

    with open(f'storage/posts/{id}.png', 'wb') as file:
        file.write(image.file.read())

    return ''

# Need to auth
@posts_router.delete('/delete/{id}')
async def deletePost(id: int, session: AsyncSession = Depends(get_async_session)):
    q = delete(PostModel).where(PostModel.id == id)
    await session.execute(q)
    await session.commit()

    return ''