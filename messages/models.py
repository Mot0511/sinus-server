from sqlalchemy import TIMESTAMP, Column, Integer, String
from auth.models import Base

class Chat(Base):
    __tablename__ = 'chats'

    id: int = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    user1: str = Column(String)
    user2: str = Column(String)

class Message(Base):
    __tablename__ = 'messages'
    
    id: int = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    chat: int = Column(Integer)
    user: str = Column(String)
    text: str = Column(String)