from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, Column, Integer, String, Table, Text, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped

metadata = MetaData()

class Base(DeclarativeBase):
    n: Mapped[int] = Column(Integer, autoincrement=True, unique=True)

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    username: str = Column(String(), unique=True)
    name: str = Column(String())
    description: str = Column(Text())

# user = Table(
#     'users',
#     metadata,
#     Column('username', String(), unique=True),
#     Column('name', String()),
#     Column('description', Text()),
#     Column('email', String(length=320), unique=True, index=True, nullable=False),
#     Column('hashed_password', String(length=1024), nullable=False),
#     Column('is_active', Boolean, default=True, nullable=False),
#     Column('is_superuser', Boolean, default=False, nullable=False),
#     Column('is_verified', Boolean, default=False, nullable=False),
# )