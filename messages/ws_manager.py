from fastapi import WebSocket

from db.models import Message


class WSManager:
    def __init__(self):
        self.chats = {}

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()

        if chat_id in self.chats:
            self.chats[chat_id].append(websocket)
        else:
            self.chats[chat_id] = [websocket]

        print(self.chats[chat_id])

    def disconnect(self, websocket: WebSocket, chat_id: int):
        self.chats[chat_id].remove(websocket)
        if not self.chats[chat_id]:
            del self.chats[chat_id]


    async def broadcast(self, message: str, chat_id: int):
        if chat_id in self.chats:
            for websocket in self.chats[chat_id]:
                await websocket.send_text(message)

manager = WSManager()