from app.events.exceptions import EventNotFound
from app.repository.events_repository import EventsRepository
from app.schemas.events.event_status import EventStatusSchema
from app.utils.services import BaseService


class EventsAdminService(BaseService):
    def __init__(self, events_repository: EventsRepository):
        self.events_repository = events_repository

    async def modify_status(self, event_id: str, new_status: EventStatusSchema):
        update_ok = await self.events_repository.update(event_id, new_status)
        if not update_ok:
            raise EventNotFound(event_id)
