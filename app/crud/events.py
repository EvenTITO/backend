
from sqlalchemy.orm import Session
from ..models.event import EventModel
from app.schemas.events import EventSchema
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException


EVENT_NOT_FOUND = 'Event not found'
ID_ALREADY_EXISTS = 'Id already exists'
TITLE_ALREADY_EXISTS = 'Title of event already exists'

def handle_database_event_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except IntegrityError as e:
            error_info = str(e.orig)
            if 'title' in error_info.lower():
                raise HTTPException(status_code=409,
                                    detail=TITLE_ALREADY_EXISTS)
            elif 'id' in error_info.lower():
                raise HTTPException(status_code=409, detail=ID_ALREADY_EXISTS)
            else:
                raise HTTPException(status_code=409, detail='Unexpected')
        except NoResultFound:
            raise HTTPException(status_code=404, detail=EVENT_NOT_FOUND)
    return wrapper


@handle_database_event_error
def get_event(db: Session, event_id: int):
    return db.query(EventModel).filter(EventModel.id == event_id).one()


@handle_database_event_error
def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EventModel).offset(skip).limit(limit).all()


@handle_database_event_error
def create_event(db: Session, event: EventSchema):
    db_event = EventModel(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@handle_database_event_error
def update_event(db: Session, event_updated: EventSchema):
    db_event = get_event(db, event_updated.id)
    for attr, value in event_updated.model_dump().items():
        setattr(db_event, attr, value)
    db.commit()
    db.refresh(db_event)
    return db_event


@handle_database_event_error
def delete_event(db: Session, event_id: str):
    # check if event exists
    event = get_event(db, event_id)
    db.delete(event)

    db.commit()

    return event

