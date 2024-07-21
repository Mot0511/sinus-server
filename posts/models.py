from auth.models import Base
from sqlalchemy import Column, Integer, MetaData, String

class Post(Base):
    __tablename__ = 'posts'

    id: int = Column(Integer, unique=True, primary_key=True)
    user: str = Column(String, unique=True)
    text: str = Column(String)