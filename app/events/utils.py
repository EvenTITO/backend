from app.events import crud, validations

# TODO: No deberia estar antes el 'validations'?
async def get_event(db, event_id):
    event = await crud.get_event_by_id(db, event_id)
    validations.validate_event_exists(event, event_id)
    return event
