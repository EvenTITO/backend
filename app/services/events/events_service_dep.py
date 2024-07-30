from fastapi import Depends
from typing import Annotated

from app.repository.events_repository import EventsRepository
from app.repository.organizers_repository import OrganizersRepository
from app.repository.repository import get_repository
from app.services.events.events_service import EventsService


class EventsChecker:
    async def __call__(
        self,
        events_repository: EventsRepository = Depends(get_repository(EventsRepository)),
        organizers_repository: OrganizersRepository = Depends(get_repository(OrganizersRepository)),
    ) -> EventsService:
        return EventsService(events_repository, organizers_repository)


events_checker = EventsChecker()
EventsServiceDep = Annotated[EventsService, Depends(events_checker)]
