from __future__ import annotations

from email.message import EmailMessage

from app.database.models.work import WorkStates
from app.repository.events_repository import EventsRepository
from app.repository.users_repository import UsersRepository
from app.schemas.members.reviewer_schema import ReviewerCreateRequestSchema
from app.services.notifications.notifications_service import NotificationsService, load_html

from fastapi import BackgroundTasks

import re

email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
CREATE_EVENT_NOTIFICATION_HTML = load_html('create-event-notification.html')
START_EVENT_NOTIFICATION_HTML = load_html('start-event-notification.html')
WAITING_APPROVAL_EVENT_NOTIFICATION_HTML = load_html('waiting-event-notification.html')
INSCRIPTION_EVENT_NOTIFICATION_HTML = load_html('inscription-event-notification.html')
INSCRIPTION_USER_EVENT_NOTIFICATION_HTML = load_html('inscription-user-event-notification.html')
REVIEWER_EVENT_NOTIFICATION_HTML = load_html('reviewer-event-notification.html')
CHANGE_WORK_STATUS_NOTIFICATION_HTML = load_html('change-work-status-notification.html')


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
        return message

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
        # Fin organizer event email
        # TODO
        # Find creator event email
        creator_id = await self.event_repository.get_creator_id(event.id)
        organizer_user = await self.users_repository.get(creator_id)
        # Find email notification emails into event
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

    def __config_common_and_send_email(self,
                                       event,
                                       emails_to_send,
                                       body_common,
                                       subject,
                                       params=None):

        self.recipients_emails = emails_to_send

        message = self.__recipients_message()

        body = self.__common_body(body_common, event)
        # Using replace parameters with [$x]
        if params is not None:
            body = self._replace_params(params, body)

        self._add_subject(message, subject)
        self._add_body(message, body, params)
        self._add_body_extra(message, body)

        return self._send_email(message)

    def __notify_event_started(self, event, emails_to_send):
        subject = f"El evento {event.title} ha sido publicado"
        self.__config_common_and_send_email(event, emails_to_send,
                                            START_EVENT_NOTIFICATION_HTML,
                                            subject)

    def __notify_event_created(self, event, emails_to_send):
        subject = "Su solicitud de creación de evento fue aprobada"
        self.__config_common_and_send_email(event, emails_to_send,
                                            CREATE_EVENT_NOTIFICATION_HTML,
                                            subject)

    def __notify_event_waiting_approval(self, event, emails_to_send):
        subject = f"El evento {event.title} ha sido enviado para su aprobación"
        self.__config_common_and_send_email(event, emails_to_send,
                                            WAITING_APPROVAL_EVENT_NOTIFICATION_HTML,
                                            subject)

    def __notify_inscription_user(self, event, subject, emails_to_send, params):
        self.__config_common_and_send_email(event, emails_to_send,
                                            INSCRIPTION_USER_EVENT_NOTIFICATION_HTML,
                                            subject,
                                            params)

    def __notify_inscription_gral(self, event, subject, emails_to_send):
        self.__config_common_and_send_email(event, emails_to_send,
                                            INSCRIPTION_EVENT_NOTIFICATION_HTML,
                                            subject)

    def __notify_new_reviewers(self, event, user_reviewer, emails_to_send, params):
        fullname = f"{user_reviewer.name} {user_reviewer.lastname}"
        subject = f"{fullname} fue asignado como reviewer"
        self.__config_common_and_send_email(event,
                                            emails_to_send,
                                            REVIEWER_EVENT_NOTIFICATION_HTML,
                                            subject,
                                            params)

    def __notify_change_work_status(self, event, emails_to_send, params):
        subject = "Su trabajo a cambiado de estado"
        self.__config_common_and_send_email(
            event,
            emails_to_send,
            CHANGE_WORK_STATUS_NOTIFICATION_HTML,
            subject,
            params)

    async def notify_event_waiting_approval(self, event):
        emails_to_send = await self.__search_emails_to_send(event)
        self.background_tasks.add_task(self.__notify_event_waiting_approval, event, emails_to_send)
        return True

    async def notify_event_created(self, event):
        emails_to_send = await self.__search_emails_to_send(event)

        self.background_tasks.add_task(self.__notify_event_created, event, emails_to_send)
        return True

    async def notify_event_started(self, event):
        emails_to_send = await self.__search_emails_to_send(event)

        self.background_tasks.add_task(self.__notify_event_started, event, emails_to_send)
        return True

    async def notify_inscription(self, event_id, user_inscripted_id):
        event = await self.event_repository.get(event_id)
        user_inscripted = await self.users_repository.get(user_inscripted_id)
        emails_to_send_gral = await self.__search_emails_to_send(event)
        user_fullname = user_inscripted.name + " " + user_inscripted.lastname

        subject = f"El usuario {user_fullname} se ha inscripto al evento {event.title}"
        self.background_tasks.add_task(self.__notify_inscription_gral, event, subject, emails_to_send_gral)

        user_inscripted_emails = user_inscripted.email
        params = [user_fullname]
        subject = f"Bienvenido a EvenTITO {user_fullname}!"
        self.background_tasks.add_task(self.__notify_inscription_user, event, subject, user_inscripted_emails, params)

        return True

    async def notify_new_reviewers(self, event_id, reviewers: ReviewerCreateRequestSchema):
        event = await self.event_repository.get(event_id)
        emails_to_send = await self.__search_emails_to_send(event)
        for reviewer in reviewers.reviewers:
            if reviewer.email is not None:
                emails_to_send.append(reviewer.email)
                user_reviewer = await self.users_repository.get_user_by_email(reviewer.email)

                fullname = f"{user_reviewer.name} {user_reviewer.lastname}"
                params = [fullname, str(reviewer.work_id), str(reviewer.review_deadline)]

                self.background_tasks.add_task(
                    self.__notify_new_reviewers,
                    event,
                    user_reviewer,
                    emails_to_send,
                    params)

        return True

    async def notify_change_work_status(self, event_id, user_id, obj, status):
        event = await self.event_repository.get(event_id)
        emails_to_send = await self.__search_emails_to_send(event)

        print(f"user_id: {user_id}")
        # TODO: sending email?
        # user = await self.users_repository.get(user_id)
        for author in obj['work'].authors:
            notify_update = author['notify_updates']
            if notify_update:
                author_email = author['mail']
                emails_to_send.append(author_email)
                print(f"email2: {author_email}")

        status_msg = ""
        if status == WorkStates.APPROVED:
            status_msg = "APROBADO"
        else:
            status_msg = "RECHAZADO"
        params = [str(obj['id']), status_msg]
        self.background_tasks.add_task(
            self.__notify_change_work_status,
            event,
            emails_to_send,
            params
        )
        return True
