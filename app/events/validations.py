from fastapi import HTTPException
from app.events import crud
from app.events.model import EventStatus
from app.users.model import UserRole
from .schemas import EventSchema
from .exceptions import (
    InvalidEventSameTitle,
    EventNotFound
)
from app.organizers.dependencies import event_organizer_checker


async def validate_event_not_exists(db, event: EventSchema):
    other_event = await crud.get_event_by_title(db, event.title)
    if other_event:
        raise InvalidEventSameTitle(event.title)


def validate_event_exists(event, event_id):
    if not event:
        raise EventNotFound(event_id)


async def validate_update(db, current_event, event_modification):
    if current_event.title != event_modification.title:
        await validate_event_not_exists(db, event_modification)


async def validate_status_change(db, caller, event, status_modification):
    if caller.role == UserRole.ADMIN:
        return
    await event_organizer_checker(event.id, caller, db)
    admin_status = [EventStatus.WAITING_APPROVAL,
                    EventStatus.NOT_APPROVED,
                    EventStatus.BLOCKED]
    if event.status in admin_status:
        raise HTTPException(status_code=403)
    if status_modification.status in admin_status:
        raise HTTPException(status_code=403)
