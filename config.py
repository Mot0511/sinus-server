import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

SECRET_JWT_WORD=os.getenv('SECRET_JWT_WORD')

DB_URI=os.getenv('POSTGRES_URL')
ALEMBIC_DB_URI=os.getenv('ALEMBIC_DB_URI')

YANDEX_EMAIL=os.getenv('YANDEX_EMAIL')
YANDEX_PASSWORD=os.getenv('YANDEX_PASSWORD')

GMAIL_EMAIL=os.getenv('GMAIL_EMAIL')
GMAIL_PASSWORD=os.getenv('GMAIL_PASSWORD')
