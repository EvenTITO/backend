from fastapi import Depends
from typing import Annotated

from app.repository.events_repository import EventsRepository
from app.repository.repository import get_repository
from app.services.events.events_configuration_service import EventsConfigurationService


class EventsConfigurationChecker:
    async def __call__(
        self,
        event_id: str,
        events_repository: EventsRepository = Depends(get_repository(EventsRepository)),
    ) -> EventsConfigurationService:
        return EventsConfigurationService(events_repository, event_id)


events_configuration_checker = EventsConfigurationChecker()
EventsConfigurationServiceDep = Annotated[EventsConfigurationService, Depends(events_configuration_checker)]
