from fastapi import Depends
from typing import Annotated

from app.repository.events_repository import EventsRepository
from app.repository.repository import get_repository
from app.services.events.events_service import EventsService


class EventServiceChecker:
    async def __call__(
        self,
        events_repository: EventsRepository = Depends(get_repository(EventsRepository)),
    ) -> EventsService:
        return EventsService(events_repository)


events_service_checker = EventServiceChecker()
EventsServiceDep = Annotated[EventsService, Depends(events_service_checker)]
