import smtplib
import ssl
from email.message import EmailMessage
from app.settings.settings import NotificationsSettings


settings = NotificationsSettings()
SLL_DEFAULT_CONTEXT = ssl.create_default_context()


class NotificationsService:
    def _send_email(self, message: EmailMessage):
        if not settings.ENABLE_SEND_EMAILS:
            return
        message['From'] = settings.NOTIFICATIONS_EMAIL
        try:
            with smtplib.SMTP_SSL(
                "smtp.gmail.com",
                settings.SMTPS_PORT,
                context=SLL_DEFAULT_CONTEXT
            ) as server:
                server.login(settings.NOTIFICATIONS_EMAIL, settings.NOTIFICATIONS_EMAIL_PASSWORD)
                server.send_message(message)
            return True
        except Exception as e:
            print(f'There was an error: {str(e)} '
                  f'sending an email: {message.as_string()}.')
            return False

    def _add_subject(self, message: EmailMessage, subject: str):
        message['Subject'] = f'[EvenTITO] {subject}'
        return message

    def _add_body(self, message: EmailMessage, body):
        if message.get_content_type() != 'text/html':
            message.set_type('text/html')

        end_text = (
            "<br><br>Este mensaje fue enviado desde "
            f"<a href='{settings.FRONTEND_URL}'>EvenTITO</a>"
        )
        body = f"{body}\n\n{end_text}"

        message.set_payload(body)
        return message
