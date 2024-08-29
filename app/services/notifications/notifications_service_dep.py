from typing import Annotated

from fastapi import Depends

from app.services.notifications.events_notifications_service import EventsNotificationsService


class EventsNotification:
    async def __call__(self) -> EventsNotificationsService:
        return EventsNotificationsService()


events_notification_service = EventsNotification()
EventsNotificationServiceDep = Annotated[
    EventsNotificationsService, Depends(events_notification_service)]
