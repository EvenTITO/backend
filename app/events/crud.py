from sqlalchemy.orm import Session
from .model import EventModel
from .schemas import EventSchema
from app.organizers.model import OrganizerModel


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


def is_creator(
    db: Session, event_id: str, user_id: str
):
    return db \
        .query(EventModel) \
        .filter(
            EventModel.id == event_id,
            EventModel.id_creator == user_id
        ).first() is not None


# def delete_event(db: Session, event_id: str):
#     event = get_event_by_id(db, event_id)
#     db.delete(event)
#     db.commit()

#     return event
