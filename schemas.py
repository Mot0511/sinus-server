from pydantic import BaseModel

class UsersPair(BaseModel):
    user1: str
    user2: str