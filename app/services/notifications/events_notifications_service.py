from app.services.notifications.notifications_service import NotificationsService


class EventsNotificationsService(NotificationsService):
    async def notify_event_approved(self, user_from, event):
        raise 'TODO'
