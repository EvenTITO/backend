import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from app.repository.users_crud import get_admin_emails

load_dotenv()

SMTPS_PORT = 465
EMAIL_PASSWORD = os.getenv('NOTIFICATIONS_EMAIL_PASSWORD')
SENDER_EMAIL = os.getenv('NOTIFICATIONS_EMAIL')
ENABLE_SEND_EMAILS = os.getenv('ENABLE_SEND_EMAILS', 'False') \
    in ["True", "true"]
FRONTEND_URL = os.getenv('FRONTEND_URL')

SLL_DEFAULT_CONTEXT = ssl.create_default_context()


def send_email(message):
    if not ENABLE_SEND_EMAILS:
        return
    message['From'] = SENDER_EMAIL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", SMTPS_PORT,
                              context=SLL_DEFAULT_CONTEXT) as server:
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(message)
    except Exception as e:
        print(f'There was an error: {str(e)} '
              f'sending an email: {message.as_string()}.')


async def message_to_admins(db):
    admins_emails = await get_admin_emails(db)
    print('los mails son', admins_emails)
    message = EmailMessage()
    message['To'] = ", ".join(admins_emails)
    return message


def create_subject(subject):
    return f'[EvenTITO] {subject}'
