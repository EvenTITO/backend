import pytest
from fastapi import BackgroundTasks

from app.database.database import SessionLocal, engine
from app.repository.events_repository import EventsRepository
from app.repository.users_repository import UsersRepository
from app.services.notifications.events_notifications_service import EventsNotificationsService
from app.settings.settings import NotificationsSettings

settings = NotificationsSettings()


class DictToObject:
    def __init__(self, dict_obj):
        for key, value in dict_obj.items():
            setattr(self, key, value)


# To run the notifications Tests, export the env variable:
# export NOTIFICATIONS_ENABLE_SEND_EMAILS=True


@pytest.mark.skipif(condition=not settings.ENABLE_SEND_EMAILS, reason="Avoid Sending many emails.")
async def test_send_notification_when_admin_approve_event(
        create_event
):
    session = SessionLocal(
        bind=engine,
    )
    create_event['notification_mails'] = ["test@test.com"]
    event = DictToObject(create_event)

    notification_service = EventsNotificationsService(
        EventsRepository(session),
        UsersRepository(session),
        BackgroundTasks())
    email_sent = await notification_service.notify_event_created(event)
    await session.close()

    assert email_sent


@pytest.mark.skipif(condition=not settings.ENABLE_SEND_EMAILS, reason="Avoid Sending many emails.")
async def test_send_notification_when_admin_approve_event_with_invalid_email(create_event):
    session = SessionLocal(
        bind=engine,
    )
    email = "string"
    create_event['notification_mails'] = [email]
    event = DictToObject(create_event)
    notification_service = EventsNotificationsService(
        EventsRepository(session),
        UsersRepository(session),
        BackgroundTasks())

    email_test = f"Format email error {email}"
    with pytest.raises(Exception) as ex:
        await notification_service.notify_event_created(event)

    await session.close()
    assert str(ex.value) == email_test
