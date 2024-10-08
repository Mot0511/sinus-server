import json
import random
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from auth.router import fastapi_users
from sqlalchemy import and_, delete, or_, select
from websockets import broadcast
from db.models import User
from auth.router import getUser
from db.models import Chat, Message as MessageModel
from messages.schemas import Message
from messages.utils import get_broadcast_message
from messages.ws_manager import WSManager
from schemas import UsersPair
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
from messages.ws_manager import manager

messages_router = APIRouter(prefix='/messages')

current_user = fastapi_users.current_user()


@messages_router.websocket('/connect/{username}/{chat_id}')
async def connect(websocket: WebSocket, chat_id: int, username: str, session: AsyncSession = Depends(get_async_session)):
    # await manager.broadcast(get_broadcast_message('in_online', username), chat_id)
    await manager.connect(websocket, chat_id)

    try:
        while True:
            wsmessage_json = await websocket.receive_text()
            wsmessage = json.loads(wsmessage_json)

            if wsmessage['type'] == 'send':
                
                while True:
                    mess_id = random.randint(1, 1000000000)
                    exists_mess_id = (await session.execute(select(MessageModel).where(MessageModel.id == mess_id))).scalar()
                    if not exists_mess_id:
                        break
                
                wsmessage['message']['id'] = mess_id
                obj = MessageModel(
                    **wsmessage['message']
                )
                
                session.add(obj)
                await session.commit()

                user = await getUser(wsmessage['message']['user'], session)
                wsmessage['message']['user'] = user.username

                broadcast_message = get_broadcast_message('new_message', json.dumps(wsmessage['message']))
                await manager.broadcast(broadcast_message, chat_id)

            
            elif wsmessage['type'] == 'remove':
                message_id = wsmessage['message']['id']

                broadcast_message = get_broadcast_message('remove_message', str(message_id))
                await manager.broadcast(broadcast_message, chat_id)

                q = delete(MessageModel).where(MessageModel.id == message_id)
                await session.execute(q)
                await session.commit()
            

    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
        await manager.broadcast(get_broadcast_message('in_offline', username), chat_id)


@messages_router.get('/get/{chat_id}')
async def getMessages(chat_id: int, session: AsyncSession = Depends(get_async_session)):
    q = select(MessageModel).where(MessageModel.chat == chat_id)
    data = await session.execute(q)
    messages = data.scalars().all()

    new_messages = []
    for message in messages:
        username = (await session.execute(select(User.username).where(User.id == message.user))).scalar()
        new_messages.append({
            **message.__dict__,
            'user': username
        })

    return new_messages


@messages_router.get('/getChats/')
async def getChats(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    q = select(Chat).where(or_(Chat.user1 == str(user.id), Chat.user2 == str(user.id)))
    data = await session.execute(q)
    chats = data.scalars().all()

    users = []
    for chat in chats:
        if chat.user1 == str(user.id):
            q = select(User).where(User.id == chat.user2)
        else:
            q = select(User).where(User.id == chat.user1)

        data = await session.execute(q)
        user = data.scalar()
        users.append(user)

    res = []
    for i in range(len(chats)):
        res.append([chats[i].id, users[i]])

    return res


@messages_router.get('/getChat/{chat_id}')
async def getChat(chat_id: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    q = select(Chat).where(and_(Chat.id == chat_id, or_(Chat.user1 == str(user.id), Chat.user2 == str(user.id))))
    data = await session.execute(q)
    chat = data.scalar()

    return chat


@messages_router.post('/addChat/{user_id}')
async def addChat(user_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    
    async def get_chat_id():
        q = select(Chat.id).where(or_(and_(Chat.user1 == str(user.id), Chat.user2 == user_id), and_(Chat.user1 == user_id, Chat.user2 == str(user.id))))
        data = await session.execute(q)
        return data.scalar()

    chat_id = await get_chat_id()

    if not chat_id:
        obj = Chat(
            user1 = str(user.id),
            user2 = user_id
        )
        session.add(obj)
        await session.commit()

        chat_id = await get_chat_id()
        return chat_id

    return chat_id


@messages_router.post('/removeChat/{id}')
async def removeChat(id: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    q_chat = delete(Chat).where(and_(Chat.id == id, or_(Chat.user1 == str(user.id), Chat.user2 == str(user.id))))
    q_messages = delete(MessageModel).where(MessageModel.chat == id)

    await session.execute(q_chat)
    await session.execute(q_messages)
    await session.commit()

