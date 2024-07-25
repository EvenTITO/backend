from app.events import validations
from app.repository import events_crud


# TODO: No deberia estar antes el 'validations'?
async def get_event(db, event_id):
    event = await events_crud.get_event_by_id(db, event_id)
    validations.validate_event_exists(event, event_id)
    return event
