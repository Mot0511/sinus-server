from fastapi import WebSocket

from messages.models import Message


class WSManager:
    def __init__(self):
        self.chats = {}

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()

        if self.chats[chat_id]:
            if not websocket in self.chats[chat_id]:
                self.chats[chat_id].append(websocket)
        else:
            self.chats = [websocket]

    def disconnect(self, websocket: WebSocket, chat_id: int):
        self.chats[chat_id].remove(websocket)
        if not self.chats:
            del self.chats[chat_id]

    async def broadcast(self, message: str, chat_id: int):
        for websocket in self.chats[chat_id]:
            await websocket.send_text(message)

manager = WSManager()