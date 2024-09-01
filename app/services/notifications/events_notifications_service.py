from email.message import EmailMessage

from app.repository.events_repository import EventsRepository
from app.repository.users_repository import UsersRepository
from app.services.notifications.notifications_service import NotificationsService, load_html

import re

email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
CREATE_EVENT_NOTIFICATION_HTML = load_html('create-event-notification.html')
START_EVENT_NOTIFICATION_HTML = load_html('start-event-notification.html')


class EventsNotificationsService(NotificationsService):
    def __init__(self, event_repository: EventsRepository, users_repository: UsersRepository):
        self.event_repository = event_repository
        self.users_repository = users_repository
        self.admins_emails = []

    def __admins_message(self):
        # Check valid format email & set emails receivers
        for email in self.admins_emails:
            if not self.__is_valid_email(email):
                raise Exception(f"Format email error {email}")
        message = EmailMessage()
        message['To'] = ",".join(self.admins_emails)
        print(message['To'])
        return message

    def __is_valid_email(self, email):
        return re.match(email_regex, email) is not None

    def __common_body(self, body, event):
        body = body.replace("[contact]", event.contact)
        body = body.replace("[title]", event.title)
        body = body.replace("[START_DATE]", event.dates[0]['date'])
        body = body.replace("[START_TIME]", event.dates[0]['time'])
        body = body.replace("[organized_by]", event.organized_by)

        return body

    def __confirm_reject_body(self, body):
        body = body.replace("[url_confirm]", "https://eventito-frontend.vercel.app/")
        body = body.replace("[url_rejected]", "https://eventito-frontend.vercel.app/")

        return body

    # Search organizer emails and extra notification emails(in event)
    async def __search_emails_to_send(self, event):

        creator_id = await self.event_repository.get_created_id_event(event.id)
        organizer_user = await self.users_repository.get(creator_id)

        emails_to_send = []
        if event.notification_mails is not None:
            emails_to_send = emails_to_send + event.notification_mails
        if organizer_user.email is not None:
            emails_to_send.append(organizer_user.email)
        return emails_to_send

    async def notify_event_created(self, event):
        self.admins_emails = await self.__search_emails_to_send(event)

        message = self.__admins_message()

        body = CREATE_EVENT_NOTIFICATION_HTML
        subject = 'Su solicitud de creación de evento fue aprobada'

        # TODO: refactor to template method
        body = self.__common_body(body, event)
        self._add_subject(message, subject)
        self._add_body(message, body)
        self._add_body_extra(message, body)

        return self._send_email(message)

    async def notify_event_started(self, event):
        self.admins_emails = self.__search_emails_to_send(event)

        message = self.__admins_message()

        body = START_EVENT_NOTIFICATION_HTML
        body = self.__common_body(body, event)

        dyn_subject = f"El evento ${event.title} se ha publicado"
        self._add_subject(message, dyn_subject)
        self._add_body(message, body)
        self._add_body_extra(message, body)

        return self._send_email(message)
