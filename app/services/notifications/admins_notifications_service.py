from email.message import EmailMessage
from app.services.notifications.notifications_service import NotificationsService, load_html

CREATE_EVENT_REQUEST_HTML = load_html('create-event-request.html')


class AdminsNotificationsService(NotificationsService):
    def __init__(self, admins_emails: list):
        self.admins_emails = admins_emails

    def request_approve_event(self, user_from, event):
        message = self.__admins_message()

        # body = f"""
        # {user_from['name']} ha solicitado crear un Evento.
        # Nombre del evento: {event['title']}
        # """
        body = CREATE_EVENT_REQUEST_HTML
        self._add_subject(message, 'Ha llegado una nueva solicitud de Creación de Evento')
        self._add_body_2(message, body)
        return self._send_email(message)

    def notify_event_approved(user_from, event):
        pass

    def __admins_message(self):
        message = EmailMessage()
        message['To'] = ", ".join(self.admins_emails)
        return message
