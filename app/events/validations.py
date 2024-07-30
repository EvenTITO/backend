from fastapi import HTTPException
from app.repository import events_crud
from app.repository import reviewers_crud as reviewers_crud
from app.database.models.event import EventStatus
from app.database.models.user import UserRole
from ..schemas.events.create_event import CreateEventSchema
from ..exceptions.events_exceptions import (
    InvalidEventSameTitle,
    EventNotFound, ReviewerFound
)
from app.organizers.dependencies import event_organizer_checker
from ..services.users.validations import validate_user_exists_with_id


async def validate_event_exists_with_id(db, event_id):
    event = await events_crud.get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(event_id)


async def validate_event_not_exists(db, event: CreateEventSchema):
    other_event = await events_crud.get_event_by_title(db, event.title)
    if other_event:
        raise InvalidEventSameTitle(event.title)


def validate_event_exists(event, event_id):
    if not event:
        raise EventNotFound(event_id)


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


async def validate_unique_reviewer(db, event_id, user_id):
    await validate_event_exists_with_id(db, event_id)
    await validate_user_exists_with_id(db, user_id)

    reviewer = await reviewers_crud.get_reviewer(db, event_id, user_id)
    print(reviewer)
    if reviewer:
        raise ReviewerFound(event_id, user_id)
