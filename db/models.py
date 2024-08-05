from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, Integer, String, Text

metadata = MetaData()

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    username: str = Column(String(), unique=True)
    name: str = Column(String())
    description: str = Column(Text())
    friends: str = Column(Text())

class Post(Base):
    __tablename__ = 'posts'

    id: int = Column(Integer, unique=True, primary_key=True)
    user: str = Column(String, unique=True)
    text: str = Column(String)

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