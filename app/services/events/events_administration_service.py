from uuid import UUID
from app.database.models.event import EventStatus
from app.database.models.user import UserRole
from app.exceptions.events_exceptions import EventNotFound, InvalidEventConfiguration, InvalidCaller
from app.repository.events_repository import EventsRepository
from app.schemas.events.dates import DatesCompleteSchema
from app.schemas.events.event_status import EventStatusSchema
from app.services.services import BaseService


class EventsAdministrationService(BaseService):
    def __init__(self, events_repository: EventsRepository):
        self.events_repository = events_repository

    async def update_status(self, event_id: UUID, new_status: EventStatusSchema, caller_role: UserRole):
        event = await self.events_repository.get(event_id)

        admin_status = [
            EventStatus.WAITING_APPROVAL,
            EventStatus.NOT_APPROVED,
            EventStatus.BLOCKED
        ]
        if (
                (caller_role != UserRole.ADMIN) and
                (event.status in admin_status or new_status.status in admin_status)
        ):
            raise InvalidCaller()

        # Check change STARTED status(publish event)
        self.all_mandatory_config_ok(event)

        if new_status.status == EventStatus.STARTED and not self.all_mandatory_config_ok(event):
            raise InvalidEventConfiguration()

        update_ok = await self.events_repository.update(event_id, new_status)
        if not update_ok:
            raise EventNotFound(event_id)

    def all_mandatory_config_ok(self, event) -> bool:
        print(event)
        event_dates = DatesCompleteSchema.model_validate(event)
        for date in event_dates.dates:
            if date.date is None and date.time is None:
                return False
        return True
