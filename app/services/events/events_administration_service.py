from fastapi import HTTPException

from app.database.models.event import EventStatus
from app.database.models.user import UserRole
from app.exceptions.events_exceptions import EventNotFound
from app.repository.events_repository import EventsRepository
from app.schemas.events.event_status import EventStatusSchema
from app.services.services import BaseService


class EventsAdministrationService(BaseService):
    def __init__(self, events_repository: EventsRepository):
        self.events_repository = events_repository

    async def update_status(self, event_id: str, new_status: EventStatusSchema, caller_role: UserRole):
        event_status = await self.events_repository.get_status(event_id)
        admin_status = [
            EventStatus.WAITING_APPROVAL,
            EventStatus.NOT_APPROVED,
            EventStatus.BLOCKED
        ]
        if (
                (caller_role != UserRole.ADMIN) and
                (event_status in admin_status or new_status.status in admin_status)
        ):
            print("error 400 no soy admin")
            raise HTTPException(status_code=400)

        update_ok = await self.events_repository.update(event_id, new_status)
        print("actualizo ok: " + str(update_ok))
        if not update_ok:
            raise EventNotFound(event_id)
