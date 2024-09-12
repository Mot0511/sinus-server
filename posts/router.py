from fastapi import APIRouter, Depends, UploadFile, Form, File, Request
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from auth.router import fastapi_users
from posts.schemas import Post
from db.models import Post as PostModel, User
from sqlalchemy import and_, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
import random


posts_router = APIRouter(prefix='/posts')

current_user = fastapi_users.current_user()


@posts_router.post('/add')
async def addPost(post: Post, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    
    obj = PostModel(
        id = post.id,
        user = str(user.id),
        text = post.text
    )
    session.add(obj)
    await session.commit()

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


@posts_router.put('/edit/{id}')
async def editPost(image: UploadFile, text = Form(), session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    
    q = update(PostModel).where(and_(PostModel.id == id, PostModel.user == str(user.id))).values(
        text = text
    )
    session.execute(q)
    await session.commit()

    with open(f'storage/posts/{id}.png', 'wb') as file:
        file.write(image.file.read())

    return ''


@posts_router.delete('/delete/{id}')
async def deletePost(id: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    q = delete(PostModel).where(and_(PostModel.id == id, PostModel.user == str(user.id)))
    await session.execute(q)
    await session.commit()

    return ''