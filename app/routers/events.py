from sqlalchemy.orm import Session
from app.utils.dependencies import SessionDep, CallerIdDep
from app.crud import events
from app.schemas.events import (
    EventSchema, CreateEventSchema,
    ModifyEventSchema, EventSchemaWithEventId,
    PublicEventsSchema
)
from fastapi import APIRouter


router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventSchemaWithEventId)
def create_event(
    event: EventSchema,
    caller_id: str = CallerIdDep,
    db: Session = SessionDep
):
    event_with_creator_id = CreateEventSchema(
        **event.model_dump(),
        id_creator=caller_id
    )
    db_event = events.create_event(db=db, event=event_with_creator_id)
    return db_event


@router.get("/{event_id}", response_model=EventSchemaWithEventId)
def read_event(event_id: str, db: Session = SessionDep):
    return events.get_event(db=db, event_id=event_id)


@router.get("/", response_model=PublicEventsSchema)
def read_all_events(db: Session = SessionDep):
    return events.get_all_events(db=db)


@router.put("/", response_model=EventSchemaWithEventId)
def update_event(
    event: EventSchemaWithEventId,
    caller_id: str = CallerIdDep,
    db: Session = SessionDep
):
    event_updated = ModifyEventSchema(
        **event.model_dump(), id_modifier=caller_id
    )
    return events.update_event(db=db, event_updated=event_updated)


@router.delete("/{event_id}", response_model=EventSchema)
def delete_event(event_id: str, db: Session = SessionDep):
    return events.delete_event(db=db, event_id=event_id)
