from sqlalchemy import TIMESTAMP, Column, Integer, String
from auth.models import Base

class Chat(Base):
    __tablename__ = 'chats'

    id: int = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    user1: str = Column(String, unique=True)
    user2: str = Column(String, unique=True)

class Message(Base):
    __tablename__ = 'messages'
    
    id: int = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    chat: int = Column(Integer, unique=True)
    user: str = Column(String, unique=True)
    text: str = Column(String)