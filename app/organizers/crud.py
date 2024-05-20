from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from .model import OrganizerModel
from .schemas import OrganizerSchema


EVENT_ORGANIZER_NOT_FOUND = "Event organizer not found."


def handle_database_organizer_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(
                status_code=404, detail=EVENT_ORGANIZER_NOT_FOUND)

    return wrapper


@handle_database_organizer_error
def get_organizer(
    db: Session, event_id: str, caller_id: str
):
    db_organizer = db \
        .query(OrganizerModel) \
        .filter(
            OrganizerModel.id_event == event_id,
            OrganizerModel.id_organizer == caller_id
        ).one()

    return db_organizer


@handle_database_organizer_error
def add_organizer_to_event(
    db: Session, new_organizer: OrganizerSchema
):
    db.add(new_organizer)
    db.commit()
    db.refresh(new_organizer)

    return new_organizer
