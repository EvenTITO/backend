from fastapi import Depends
from typing import Annotated

from app.repository.events_repository import EventsRepository
from app.repository.repository import get_repository
from app.services.events.events_administration_service import EventsAdministrationService
from app.services.notifications.events_notifications_service import EventsNotificationsService
from app.services.notifications.notifications_service_dep import EventsNotificationServiceDep


class EventsAdministartionServiceChecker:
    async def __call__(
        self,
        events_repository: EventsRepository = Depends(get_repository(EventsRepository)),
        events_Notifications_service: EventsNotificationsService = Depends(EventsNotificationServiceDep)
    ) -> EventsAdministrationService:
        return EventsAdministrationService(events_repository, events_Notifications_service)


events_administrations_checker = EventsAdministartionServiceChecker()
EventsAdministrationServiceDep = Annotated[EventsAdministrationService, Depends(events_administrations_checker)]
