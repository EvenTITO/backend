from fastapi import HTTPException

from app.database.models.event import EventStatus
from app.database.models.user import UserRole
from app.exceptions.events_exceptions import EventNotFound, InvalidEventSameTitle
from app.repository.events_repository import EventsRepository
from app.schemas.events.configuration import EventConfigurationSchema
from app.schemas.events.create_event import CreateEventSchema
from app.schemas.events.public_event_with_roles import PublicEventWithRolesSchema
from app.schemas.events.schemas import EventRol
from app.services.event_organizers.event_organizers_service import EventOrganizersService
from app.services.services import BaseService


class EventsService(BaseService):
    def __init__(self, events_repository: EventsRepository, organizers_service: EventOrganizersService):
        self.events_repository = events_repository
        self.organizers_service = organizers_service

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

        # TODO: add notifications in events_service if if event_created.status == EventStatus.WAITING_APPROVAL.

    async def get_my_events(self, caller_id: str, offset: int, limit: int) -> list[PublicEventWithRolesSchema]:
        return await self.events_repository.get_all_events_for_user(caller_id, offset=offset, limit=limit)

    async def get_all_events(
            self,
            offset: int,
            limit: int,
            status: EventStatus | None,
            title_search: str | None,
            user_role: UserRole
    ):
        if status != EventStatus.STARTED and user_role != UserRole.ADMIN:
            raise HTTPException(status_code=400)  # TODO: change to custom exception.

        return await self.events_repository.get_all_events(offset, limit, status, title_search)

    async def get_public_event(self, caller_id: str | None, event_id: str):
        event = await self.events_repository.get(event_id)
        if event is None:
            raise EventNotFound(event_id)
        event = PublicEventWithRolesSchema.model_validate(event)
        if caller_id is None:
            return event
        if await self.organizers_service.is_organizer(event_id, caller_id):
            event.roles.append(EventRol.ORGANIZER)
        return event

    async def get_event_status(self, event_id: str):
        event_status = await self.events_repository.get_status(event_id)
        if event_status is None:
            raise EventNotFound(event_id)
        return event_status
