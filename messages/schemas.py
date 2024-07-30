from pydantic import BaseModel
from sqlalchemy import TIMESTAMP


class Message(BaseModel):
    id: int
    chat: int
    user: str
    text: str