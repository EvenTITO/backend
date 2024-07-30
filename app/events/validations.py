from app.repository import events_crud
from app.repository import reviewers_crud as reviewers_crud
from ..schemas.events.create_event import CreateEventSchema
from ..exceptions.events_exceptions import (
    InvalidEventSameTitle,
    EventNotFound, ReviewerFound
)
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


async def validate_unique_reviewer(db, event_id, user_id):
    await validate_event_exists_with_id(db, event_id)
    await validate_user_exists_with_id(db, user_id)

    reviewer = await reviewers_crud.get_reviewer(db, event_id, user_id)
    print(reviewer)
    if reviewer:
        raise ReviewerFound(event_id, user_id)
