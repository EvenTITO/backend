from typing import Union
from fastapi import HTTPException
from app.database.models.event import EventStatus
from app.events.exceptions import EventNotFound
from app.repository.events_repository import EventsRepository
from app.schemas.events.event_status import EventStatusSchema
from app.schemas.events.schemas import EventRol
from app.services.services import BaseService
from app.database.models.user import UserRole


class EventsService(BaseService):
    def __init__(self, events_repository: EventsRepository):
        self.events_repository = events_repository

    async def modify_status(self, event_id: str, new_status: EventStatusSchema, caller_role: Union[EventRol, UserRole]):
        print('staaat', new_status)
        event_status = await self.events_repository.get_status(event_id)
        print('uy', event_status)
        admin_status = [
            EventStatus.WAITING_APPROVAL,
            EventStatus.NOT_APPROVED,
            EventStatus.BLOCKED
        ]
        if (
            (caller_role != UserRole.ADMIN) and
            (event_status in admin_status or new_status.status in admin_status)
        ):
            print('el rol es', caller_role)
            print('el rol es', caller_role)
            raise HTTPException(status_code=400)
        print('esa', event_status)

        update_ok = await self.events_repository.update(event_id, new_status)
        print('el new status es', new_status)
        if not update_ok:
            raise EventNotFound(event_id)
