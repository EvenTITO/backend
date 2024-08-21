from fastapi import Depends
from typing import Annotated

from app.repository.events_repository import EventsRepository
from app.repository.repository import get_repository
from app.services.events.events_administration_service import EventsAdministrationService


class EventsAdministartionServiceChecker:
    async def __call__(
        self,
        events_repository: EventsRepository = Depends(get_repository(EventsRepository)),
    ) -> EventsAdministrationService:
        return EventsAdministrationService(events_repository)


events_administrations_checker = EventsAdministartionServiceChecker()
EventsAdministrationServiceDep = Annotated[EventsAdministrationService, Depends(events_administrations_checker)]
