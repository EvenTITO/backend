import pytest
from app.services.notifications.admins_notifications_service import AdminsNotificationsService
from app.settings.settings import NotificationsSettings

settings = NotificationsSettings()


# To run the notifications Tests, export the env variable:
# export ENABLE_SEND_EMAILS=True

@pytest.mark.skipif(condition=not settings.ENABLE_SEND_EMAILS, reason="Avoid Sending many emails.")
async def test_send_notification():
    notification_service = AdminsNotificationsService(['mateocapon@gmail.com', 'fsinisi@fi.uba.ar', 'mcapon@fi.uba.ar'])
    user_from = {
        'name': 'mateo'
    }
    event = {
        'title': 'repiola'
    }
    email_sended = notification_service.request_approve_event(user_from, event)
    assert email_sended
