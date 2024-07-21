from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped

metadata = MetaData()

class Base(DeclarativeBase):
    pass

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