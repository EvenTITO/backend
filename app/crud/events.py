from sqlalchemy.orm import Session
from ..models.event import EventModel
from app.schemas.events import EventSchema


def get_event(db: Session, event_id: int):
    return db.query(EventModel).filter(EventModel.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EventModel).offset(skip).limit(limit).all()


def get_event_by_name(db: Session, event_name: str):
    return db.query(EventModel).filter(EventModel.name == event_name).first()


def create_event(db: Session, event: EventSchema):
    db_event = EventModel(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
