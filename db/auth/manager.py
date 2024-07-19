from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from db.db import get_user_db
from db.models import User
from config import SECRET_JWT_WORD
import json
import smtplib

from utils.get_email_template import get_email_template


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET_JWT_WORD
    verification_token_secret = SECRET_JWT_WORD

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        print(f'User {user.id} has registered')
    
    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None) -> None:
        print()

        email = user.email

        service = email.split('@')[1].split('.')[0]
        
        if service == 'gmail':
            print(1)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('suvorovmatvej9@gmail.com', 'pifu wamh agfx cxyw')

        elif service == 'yandex':
            print(2)
            s = smtplib.SMTP('smtp.yandex.ru', 587)
            s.starttls()
            s.login('Mat0511@yandex.ru', 'Y_browserplusmusic2')
    
        # message_template = get_email_template('reset_password')
        # message = message_template.substitude(TOKEN=token)

        message = f'<a href="http://localhost:3000/signin/reset_password/{token}">Восстановить пароль</a>'
    
        letter = MIMEText(message, 'html')

        letter['From'] = 'support@sinus.ru'
        letter['To'] = email
        letter['Subject'] = "Восстановление пароля на Sinus"

        s.sendmail('support@sinus.ru', email, letter.as_string())
        s.quit()


    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None) -> None:
        print(f"Verification requested for user {user.id}")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)