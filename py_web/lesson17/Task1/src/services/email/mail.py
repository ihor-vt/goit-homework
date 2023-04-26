from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service
from src.conf.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=EmailStr(settings.mail_username),
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Rest API App",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)


async def send_email(email: EmailStr, username: str, host: str, subj: str = "Confirm your email "):
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject=subj,
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html
        )
        
        fm = FastMail(conf)
        if subj == "Confirm your email ":
            await fm.send_message(message, template_name="email_template.html")
        elif subj == "Reset your password ":
            await fm.send_message(message, template_name="email_template_reset_password.html")
    except ConnectionErrors as err:
        print(f">>> mail.py {err}")
