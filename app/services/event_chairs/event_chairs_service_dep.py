from typing import Annotated

from fastapi import Depends

from app.repository.chairs_repository import ChairRepository
from app.repository.repository import get_repository
from app.repository.users_repository import UsersRepository
from app.services.event_chairs.event_chairs_service import EventChairService


class EventsChairChecker:
    async def __call__(
            self,
            users_repository: UsersRepository = Depends(get_repository(UsersRepository)),
            chair_repository: ChairRepository = Depends(get_repository(ChairRepository)),
    ) -> EventChairService:
        return EventChairService(chair_repository, users_repository)


event_chair_checker = EventsChairChecker()
EventChairServiceDep = Annotated[EventChairService, Depends(event_chair_checker)]
