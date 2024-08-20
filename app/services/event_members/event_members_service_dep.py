from typing import Annotated

from fastapi import Depends

from app.repository.chairs_repository import ChairRepository
from app.repository.organizers_repository import OrganizerRepository
from app.repository.repository import get_repository
from app.repository.users_repository import UsersRepository
from app.services.event_members.event_members_service import EventMembersService


class EventsMemberChecker:
    async def __call__(
            self,
            users_repository: UsersRepository = Depends(get_repository(UsersRepository)),
            organizers_repository: OrganizerRepository = Depends(get_repository(OrganizerRepository)),
            chair_repository: ChairRepository = Depends(get_repository(ChairRepository)),
    ) -> EventMembersService:
        return EventMembersService(organizers_repository, chair_repository, users_repository)


event_members_checker = EventsMemberChecker()
EventMembersServiceDep = Annotated[EventMembersService, Depends(event_members_checker)]
