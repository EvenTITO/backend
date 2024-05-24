from app.events import crud, validations


def get_event(db, event_id):
    event = crud.get_event_by_id(db, event_id)
    validations.validate_event_exists(event, event_id)
    return event
