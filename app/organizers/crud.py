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


def is_organizer(
    db: Session, event_id: str, caller_id: str
):
    return db \
        .query(OrganizerModel) \
        .filter(
            OrganizerModel.id_event == event_id,
            OrganizerModel.id_organizer == caller_id
        ).first() is not None


@handle_database_organizer_error
def add_organizer_to_event(
    db: Session, new_organizer: OrganizerSchema
):
    new_organizer = OrganizerModel(**new_organizer.model_dump())
    db.add(new_organizer)
    db.commit()
    db.refresh(new_organizer)

    return new_organizer
