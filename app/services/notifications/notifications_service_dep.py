from typing import Annotated

from fastapi import Depends

from app.repository.events_repository import EventsRepository
from app.repository.repository import get_repository
from app.repository.users_repository import UsersRepository
from app.services.notifications.events_notifications_service import EventsNotificationsService


class EventsNotification:
    async def __call__(
        self,
        events_repository: EventsRepository = Depends(get_repository(EventsRepository)),
        users_repository: UsersRepository = Depends(get_repository(UsersRepository))
    ) -> EventsNotificationsService:
        return EventsNotificationsService(events_repository, users_repository)


events_notification_service = EventsNotification()
EventsNotificationServiceDep = Annotated[
    EventsNotificationsService, Depends(events_notification_service)]
