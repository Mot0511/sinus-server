import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DB=os.getenv('DB')
SECRET_JWT_WORD=os.getenv('SECRET_JWT_WORD')