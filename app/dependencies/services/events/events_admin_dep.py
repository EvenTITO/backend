from fastapi import Depends
from typing import Annotated

from app.dependencies.repository.repository import get_repository
from app.authorization.admin_user_dep import AdminDep
from app.repository.events_repository import EventsRepository
from app.services.events.events_admin_service import EventsAdminService


class EventsAdmin:
    async def __call__(
        self,
        _: AdminDep,
        events_repository: EventsRepository = Depends(get_repository(EventsRepository)),
    ) -> EventsAdminService:
        return EventsAdminService(events_repository)


author_works_service = EventsAdmin()
EventsAdminServiceDep = Annotated[EventsAdminService, Depends(author_works_service)]
