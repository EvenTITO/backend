from sqlalchemy.orm import Session
from app.models.event import EventModel
from app.models.event_organizer import EventOrganizerModel
from app.schemas.events import CreateEventSchema, ModifyEventSchema
from app.utils.exceptions import DatesException
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException
import logging

EVENT_NOT_FOUND = "Event not found"
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
            else:
                logging.log(logging.ERROR, f"unexpected_error: {str(e)}")
                raise HTTPException(status_code=409, detail="Unexpected")
        except NoResultFound:
            raise HTTPException(status_code=404, detail=EVENT_NOT_FOUND)
        except DatesException as e:
            raise HTTPException(status_code=400, detail=e.error_message)

    return wrapper


@handle_database_event_error
def get_event(db: Session, event_id: int):
    return db.query(EventModel).filter(EventModel.id == event_id).one()


@handle_database_event_error
def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EventModel).offset(skip).limit(limit).all()


@handle_database_event_error
def create_event(db: Session, event: CreateEventSchema):
    db_event = EventModel(**event.model_dump())
    db.add(db_event)
    db.flush()

    organizer = EventOrganizerModel(
        id_organizer=event.id_creator, id_event=db_event.id)
    db.add(organizer)
    db.commit()
    db.refresh(db_event)
    return db_event


@handle_database_event_error
def update_event(db: Session, event_updated: ModifyEventSchema):
    db_event = get_event(db, event_updated.id)
    for attr, value in event_updated.model_dump().items():
        setattr(db_event, attr, value)
    db.commit()

    return db_event


@handle_database_event_error
def delete_event(db: Session, event_id: str):
    event = get_event(db, event_id)
    db.delete(event)
    db.commit()

    return event
