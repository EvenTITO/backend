from fastapi import HTTPException
from app.database.models.event import EventStatus
from app.database.models.user import UserRole
from app.exceptions.events_exceptions import InvalidEventSameTitle
from app.repository.events_repository import EventsRepository
from app.schemas.events.configuration import EventConfigurationSchema
from app.schemas.events.create_event import CreateEventSchema
from app.schemas.events.public_event_with_roles import PublicEventWithRolesSchema
from app.services.services import BaseService


class EventsService(BaseService):
    def __init__(self, events_repository: EventsRepository):
        self.events_repository = events_repository

    async def create(self, event: CreateEventSchema, creator_id: str, user_role: UserRole):
        event_same_title_exists = await self.events_repository.event_with_title_exists(event.title)
        if event_same_title_exists:
            raise InvalidEventSameTitle(event.title)

        if user_role == UserRole.EVENT_CREATOR:
            status = EventStatus.CREATED
        else:
            status = EventStatus.WAITING_APPROVAL

        event = EventConfigurationSchema(
            **event.model_dump(mode='json'),
            status=status
        )
        event_created = await self.events_repository.create(creator_id, event)
        return event_created.id

    async def get_my_events(self, caller_id: str, offset: int, limit: int) -> list[PublicEventWithRolesSchema]:
        return await self.events_repository.get_all_events_for_user(caller_id, offset=offset, limit=limit)

    async def get_all_events(self, offset: int, limit: int, status: EventStatus | None, title_search: str | None, user_role: UserRole):
        if (status != EventStatus.STARTED and user_role != UserRole.ADMIN):
            raise HTTPException(status_code=400)  # TODO: change to custom exception.

        return await self.events_repository.get_all_events(offset, limit, status, title_search)
