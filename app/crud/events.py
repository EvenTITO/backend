from sqlalchemy.orm import Session
from app.models.event import EventModel
from app.models.event_organizer import EventOrganizerModel
from app.schemas.events import (
    CreateEventSchema,
    ModifyEventSchema,
    PublicEventsSchema
)
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


@handle_database_event_error
def get_event(db: Session, event_id: str):
    return db.query(EventModel).filter(EventModel.id == event_id).one()


@handle_database_event_error
def get_all_events(db: Session, offset: int, limit: int):
    events = db.query(EventModel).offset(offset).limit(limit).all()
    events_dicts = [event.to_dict() for event in events]
    return PublicEventsSchema(events=events_dicts)


@handle_database_event_error
def create_event(db: Session, event: CreateEventSchema) -> EventModel:
    db_event = EventModel(**event.model_dump())
    db.add(db_event)
    db.flush()

    organizer = EventOrganizerModel(
        id_organizer=event.id_creator, id_event=db_event.id
    )
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
