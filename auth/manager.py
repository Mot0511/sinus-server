from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from db.db import get_user_db
from auth.models import User
from config import GMAIL_EMAIL, GMAIL_PASSWORD, SECRET_JWT_WORD, YANDEX_EMAIL, YANDEX_PASSWORD
import json
import smtplib
import shutil
from utils.get_email_template import get_email_template


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET_JWT_WORD
    verification_token_secret = SECRET_JWT_WORD

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        shutil.copyfile('storage/default_avatar.png', f'storage/avatars/{user.id}.png')
    
    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None) -> None:
        email = user.email

        service = email.split('@')[1].split('.')[0]
        
        if service == 'gmail':
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(GMAIL_EMAIL, GMAIL_PASSWORD)

        elif service == 'yandex':
            s = smtplib.SMTP('smtp.yandex.ru', 587)
            s.starttls()
            s.login(YANDEX_EMAIL, YANDEX_PASSWORD)
    
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