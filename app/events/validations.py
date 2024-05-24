from app.events import crud
from .schemas import EventSchema
from .exceptions import (
    InvalidEventSameTitle,
    EventNotFound
)


def validate_event_not_exists(db, event: EventSchema):
    other_event = crud.get_event_by_title(db, event.title)
    if other_event:
        raise InvalidEventSameTitle(event.title)


def validate_event_exists(event, event_id):
    if not event:
        raise EventNotFound(event_id)


def validate_update(db, current_event, event_modification):
    if current_event.title != event_modification.title:
        validate_event_not_exists(db, event_modification)
