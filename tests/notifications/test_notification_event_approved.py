import pytest

from app.services.notifications.events_notifications_service import EventsNotificationsService
from app.settings.settings import NotificationsSettings

settings = NotificationsSettings()


# To run the notifications Tests, export the env variable:
# export NOTIFICATIONS_ENABLE_SEND_EMAILS=True

@pytest.mark.skipif(condition=not settings.ENABLE_SEND_EMAILS, reason="Avoid Sending many emails.")
async def test_send_notification_when_admin_approve_event(create_event_with_email):

    notification_service = EventsNotificationsService()
    email_sent = await notification_service.notify_event_approved(create_event_with_email)
    print(email_sent)
    assert email_sent


@pytest.mark.skipif(condition=not settings.ENABLE_SEND_EMAILS, reason="Avoid Sending many emails.")
async def test_send_notification_when_admin_approve_event_with_invalid_email():
    notification_service = EventsNotificationsService()
    email_test = "Format email error string"
    with pytest.raises(Exception) as ex:
        await notification_service.notify_event_approved(["string"])
    assert str(ex.value) == email_test
    print(email_test)
