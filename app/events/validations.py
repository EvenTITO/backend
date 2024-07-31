from ..exceptions.events_exceptions import (
    EventNotFound
)


def validate_event_exists(event, event_id):
    if not event:
        raise EventNotFound(event_id)
