from email.message import EmailMessage
from app.services.notifications.notifications_service import NotificationsService


class AdminsNotificationsService(NotificationsService):
    def __init__(self, admins_emails: list):
        self.admins_emails = admins_emails

    def request_approve_event(self, user_from, event):
        message = self.__admins_message()

        body = f"""
        {user_from['name']} ha solicitado crear un Evento.
        Nombre del evento: {event['title']}
        """

        message['Subject'] = 'Ha llegado una nueva solicitud de Creación de Evento'

        message.set_content(body)
        return self.send_email(message)

    def notify_event_approved(user_from, event):
        pass

    def __admins_message(self):
        message = EmailMessage()
        message['To'] = ", ".join(self.admins_emails)
        return message
