from fastapi import Depends
from typing import Annotated

from app.repository.organizers_repository import OrganizerRepository
from app.repository.repository import get_repository
from app.repository.users_repository import UsersRepository
from app.services.event_organizers.event_organizers_service import EventOrganizersService


class EventsOrganizerChecker:
    async def __call__(
        self,
        users_repository: UsersRepository = Depends(get_repository(UsersRepository)),
        organizers_repository: OrganizerRepository = Depends(get_repository(OrganizerRepository)),
    ) -> EventOrganizersService:
        return EventOrganizersService(organizers_repository, users_repository)


event_organizers_checker = EventsOrganizerChecker()
EventOrganizersServiceDep = Annotated[EventOrganizersService, Depends(event_organizers_checker)]
