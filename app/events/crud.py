from sqlalchemy.orm import Session
from .model import EventModel
from .schemas import (
    EventSchema
)
from app.organizers.model import OrganizerModel
from app.utils.exceptions import DatesException
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException
import logging

EVENT_NOT_FOUND = "Event not found"
USER_NOT_FOUNT = "User not found"
ID_ALREADY_EXISTS = "Id already exists"
TITLE_ALREADY_EXISTS = "Title of event already exists"
CREATOR_NOT_EXISTS = "The Creator does not exist"


def handle_database_event_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except IntegrityError as e:
            error_info = str(e.orig)
            if "title" in error_info.lower():
                raise HTTPException(
                    status_code=409, detail=TITLE_ALREADY_EXISTS)
            elif "id_creator" in error_info.lower():
                raise HTTPException(status_code=409, detail=CREATOR_NOT_EXISTS)
            elif "id_event" in error_info.lower():
                raise HTTPException(status_code=409, detail=EVENT_NOT_FOUND)
            elif "id_suscriptor" in error_info.lower():
                raise HTTPException(status_code=409, detail=USER_NOT_FOUNT)

            else:
                logging.log(logging.ERROR, f"unexpected_error: {str(e)}")
                raise HTTPException(status_code=409, detail="Unexpected")
        except NoResultFound:
            raise HTTPException(status_code=404, detail=EVENT_NOT_FOUND)
        except DatesException as e:
            raise HTTPException(status_code=400, detail=e.error_message)

    return wrapper


def get_event_by_id(db: Session, event_id: str):
    return db.query(EventModel).filter(EventModel.id == event_id).first()


def get_event_by_title(db: Session, event_title: str):
    return db.query(EventModel).filter(EventModel.title == event_title).first()


def get_all_events(db: Session, offset: int, limit: int):
    return db.query(EventModel).offset(offset).limit(limit).all()


def create_event(db: Session, event: EventSchema, id_creator: str):
    db_event = EventModel(**event.model_dump(), id_creator=id_creator)
    db.add(db_event)
    db.flush()

    db_organizer = OrganizerModel(
        id_organizer=id_creator,
        id_event=db_event.id
    )
    db.add(db_organizer)
    db.flush()

    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(
    db: Session,
    current_event: EventModel,
    event_modification: EventSchema
):
    for attr, value in event_modification.model_dump().items():
        setattr(current_event, attr, value)
    db.commit()
    db.refresh(current_event)

    return current_event


@handle_database_event_error
def delete_event(db: Session, event_id: str):
    event = get_event_by_id(db, event_id)
    db.delete(event)
    db.commit()

    return event


def is_creator(
    db: Session, event_id: str, user_id: str
):
    return db \
        .query(EventModel) \
        .filter(
            EventModel.id == event_id,
            EventModel.id_creator == user_id
        ).first() is not None
