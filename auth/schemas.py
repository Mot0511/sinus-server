from typing import Optional
import uuid
from fastapi_users import schemas

class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    name: str
    description: str

class UserCreate(schemas.BaseUserCreate):
    username: str
    name: str
    description: str

class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None