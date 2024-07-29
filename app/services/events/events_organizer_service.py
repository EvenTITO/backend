from fastapi import HTTPException
from app.models.event import EventStatus
from app.repository.events_repository import EventsRepository
from app.schemas.events.event_status import EventStatusSchema
from app.utils.services import BaseService


class EventsOrganizerService(BaseService):
    def __init__(self, events_repository: EventsRepository, event_id: str, user_id: str):
        self.events_repository = events_repository
        self.event_id = event_id
        self.user_id = user_id

    async def modify_status(self, event_id: str, new_status: EventStatusSchema):
        assert event_id == self.event_id, 'Event Id should be the same, as this service is for the event Organizer.'
        event_status = await self.events_repository.get_status(event_id)
        admin_status = [
            EventStatus.WAITING_APPROVAL,
            EventStatus.NOT_APPROVED,
            EventStatus.BLOCKED
        ]
        if event_status in admin_status or new_status.status in admin_status:
            raise HTTPException(status_code=403)

        await self.events_repository.update(event_id, new_status)
