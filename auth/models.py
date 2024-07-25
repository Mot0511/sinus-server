from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, Text
from db.models import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    username: str = Column(String(), unique=True)
    name: str = Column(String())
    description: str = Column(Text())
    friends: str = Column(Text())