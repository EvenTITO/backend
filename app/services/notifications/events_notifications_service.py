from email.message import EmailMessage

from app.repository.events_repository import EventsRepository
from app.repository.users_repository import UsersRepository
from app.services.notifications.notifications_service import NotificationsService, load_html

from fastapi import BackgroundTasks

import re

email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
CREATE_EVENT_NOTIFICATION_HTML = load_html('create-event-notification.html')
START_EVENT_NOTIFICATION_HTML = load_html('start-event-notification.html')
WAITING_APPROVAL_EVENT_NOTIFICATION_HTML = load_html('waiting-event-notification.html')


class EventsNotificationsService(NotificationsService):
    def __init__(self,
                 event_repository: EventsRepository,
                 users_repository: UsersRepository,
                 background_tasks: BackgroundTasks):
        self.event_repository = event_repository
        self.users_repository = users_repository
        self.recipients_emails = []
        self.background_tasks = background_tasks

    def __recipients_message(self):
        message = EmailMessage()
        message['To'] = ",".join(self.recipients_emails)
        print(message['To'])
        return message

    def __validate_emails(self, emails):
        # Check emails size
        if len(emails) == 0:
            raise Exception("Emails to send is empty")
        # Check valid format email & set emails receivers
        for email in emails:
            if not self.__is_valid_email(email):
                raise Exception(f"Format email error {email}")

    def __is_valid_email(self, email):
        return re.match(email_regex, email) is not None

    def __common_body(self, body, event):
        start_date = "Sin definir"
        start_time = "Sin definir"
        organized_by = "Sin definir"
        if event.dates[0]['date'] is not None:
            start_date = event.dates[0]['date']
        if event.dates[0]['date'] is not None:
            start_time = event.dates[0]['time']
        if event.organized_by is not None:
            organized_by = event.organized_by

        body = body.replace("[contact]", event.contact)
        body = body.replace("[title]", event.title)
        body = body.replace("[START_DATE]", start_date)
        body = body.replace("[START_TIME]", start_time)
        body = body.replace("[organized_by]", organized_by)

        return body

    def __confirm_reject_body(self, body):
        body = body.replace("[url_confirm]", "https://eventito-frontend.vercel.app/")
        body = body.replace("[url_rejected]", "https://eventito-frontend.vercel.app/")

        return body

    # Search organizer emails and extra notification emails(in event)
    async def __search_emails_to_send(self, event):
        creator_id = await self.event_repository.get_creator_id(event.id)
        organizer_user = await self.users_repository.get(creator_id)

        emails_to_send = []
        if event.notification_mails is not None:
            emails_to_send = emails_to_send + event.notification_mails
        if organizer_user is not None:
            if organizer_user.email is not None:
                emails_to_send.append(organizer_user.email)
        return emails_to_send

    def __print_email(self, emails, message):
        print(f"Sending emails to {emails}")
        print("email message:")
        print(f"{message}")

    def __notify_event_started(self, event, emails_to_send):
        self.recipients_emails = emails_to_send

        message = self.__recipients_message()

        body = START_EVENT_NOTIFICATION_HTML
        body = self.__common_body(body, event)

        dyn_subject = f"El evento {event.title} se ha publicado"
        self._add_subject(message, dyn_subject)
        self._add_body(message, body)
        self._add_body_extra(message, body)

        self.__print_email(emails_to_send, message)
        return self._send_email(message)

    def __notify_event_created(self, event, emails_to_send):
        self.recipients_emails = emails_to_send
        if len(self.recipients_emails) == 0:
            print("Non-existent email recipients")
            return

        message = self.__recipients_message()

        body = CREATE_EVENT_NOTIFICATION_HTML
        subject = 'Su solicitud de creación de evento fue aprobada'

        # TODO: refactor to template method
        body = self.__common_body(body, event)
        self._add_subject(message, subject)
        self._add_body(message, body)
        self._add_body_extra(message, body)

        self.__print_email(emails_to_send, message)
        return self._send_email(message)

    def __notify_event_waiting_approval(self, event, emails_to_send):
        self.recipients_emails = emails_to_send
        print(self.recipients_emails)
        if len(self.recipients_emails) == 0:
            print("Non-existent email recipients")
            return
        message = self.__recipients_message()

        body = WAITING_APPROVAL_EVENT_NOTIFICATION_HTML
        body = self.__common_body(body, event)

        dyn_subject = f"El evento {event.title} se ha enviado para su aprobación"
        self._add_subject(message, dyn_subject)
        self._add_body(message, body)
        self._add_body_extra(message, body)

        self.__print_email(emails_to_send, message)

        return self._send_email(message)

        # message = self.__recipients_message()
        # print("[TEST] 1")
        # return self.send_email2(message)

    async def notify_event_waiting_approval(self, event):
        emails_to_send = await self.__search_emails_to_send(event)
        self.__validate_emails(emails_to_send)

        self.background_tasks.add_task(self.__notify_event_waiting_approval, event, emails_to_send)
        return True

    async def notify_event_created(self, event):
        emails_to_send = await self.__search_emails_to_send(event)
        self.__validate_emails(emails_to_send)

        self.background_tasks.add_task(self.__notify_event_created, event, emails_to_send)
        return True

    async def notify_event_started(self, event):
        emails_to_send = await self.__search_emails_to_send(event)
        self.__validate_emails(emails_to_send)

        self.background_tasks.add_task(self.__notify_event_started, event, emails_to_send)
        return True
