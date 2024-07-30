import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import delete, select
from websockets import broadcast
from messages.models import Chat, Message as MessageModel
from messages.schemas import Message
from messages.utils import get_broadcast_message
from messages.ws_manager import WSManager
from schemas import UsersPair
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
from messages.ws_manager import manager

messages_router = APIRouter(prefix='/messages')

@messages_router.websocket('/connect/{username}/{chat_id}')
async def connect(websocket: WebSocket, chat_id: int, username: str, session: AsyncSession = Depends(get_async_session)):
    await manager.connect(websocket, chat_id)
    await manager.broadcast(get_broadcast_message('in_online', username), chat_id)

    try:
        while True:
            wsmessage_json = await websocket.receive_text()
            wsmessage = json.loads(wsmessage_json)

            if wsmessage['type'] == 'send':
                broadcast_message = get_broadcast_message('new_message', json.dumps(wsmessage['message']))
                await manager.broadcast(broadcast_message, chat_id)

                message = wsmessage['message']
                obj = MessageModel(
                    **message
                )
                session.add(obj)
                await session.commit()
            
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

    return messages

@messages_router.get('/getChats/{user_id}')
async def getChats(user_id: str, session: AsyncSession = Depends(get_async_session)):
    q = select(Chat).where(Chat.user1 == user_id or Chat.user2 == user_id)
    data = await session.execute(q)
    chats = data.scalars().all()

    return chats

@messages_router.post('/addChat')
async def addChat(users: UsersPair, session: AsyncSession = Depends(get_async_session)):
    obj = Chat(
        user1 = users.user1,
        user2 = users.user2
    )
    await session.add(obj)
    await session.commit()

@messages_router.post('/removeChat/{id}')
async def removeChat(id: int, session: AsyncSession = Depends(get_async_session)):
    q_chat = delete(Chat).where(Chat.id == id)
    q_messages = delete(MessageModel).where(Chat.chat == id)

    await session.execute(q_chat)
    await session.execute(q_messages)
    await session.commit()

