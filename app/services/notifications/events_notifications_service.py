from email.message import EmailMessage

from app.services.notifications.admins_notifications_service import CREATE_EVENT_REQUEST_HTML
from app.services.notifications.notifications_service import NotificationsService

import re

email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


class EventsNotificationsService(NotificationsService):
    def __init__(self):
        self.admins_emails = None

    def __admins_message(self):
        # Check valid format email
        for email in self.admins_emails:
            if not self.__is_valid_email(email):
                raise Exception(f"Format email error {email}")
        message = EmailMessage()
        message['To'] = ", ".join(self.admins_emails)
        return message

    def __is_valid_email(self, email):
        return re.match(email_regex, email) is not None

    async def notify_event_approved(self, event):
        print(event)
        self.admins_emails = event['notification_mails']

        message = self.__admins_message()

        # body = f"""
        # {user_from['name']} ha solicitado crear un Evento.
        # Nombre del evento: {event['title']}
        # """
        body = CREATE_EVENT_REQUEST_HTML
        body = self.__complete_body(body, event)
        self._add_subject(message, 'Ha llegado una nueva solicitud de Creación de Evento')
        self._add_body(message, body)

        self._add_body_2(message, body)

        return self._send_email(message)

    def __complete_body(self, body, event):
        print(event)
        body = body.replace("[contact]", event['contact'])
        body = body.replace("[title]", event['title'])
        body = body.replace("[START_DATE]", event['dates'][0]['date'])
        body = body.replace("[START_TIME]", event['dates'][0]['time'])
        body = body.replace("[organized_by]", event['organized_by'])

        body = body.replace("[url_confirm]", "https://eventito-frontend.vercel.app/")
        body = body.replace("[url_rejected]", "https://eventito-frontend.vercel.app/")

        return body
