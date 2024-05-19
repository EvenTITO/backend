from sqlalchemy.orm import Session
from app.utils.dependencies import get_db, get_user_id
from app.crud import events
from app.schemas.events import (
    EventSchema, CreateEventSchema,
    ModifyEventSchema, EventSchemaWithEventId
)
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventSchemaWithEventId)
def create_event(
    event: EventSchema,
    creator_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    event_with_creator_id = CreateEventSchema(
        **event.model_dump(),
        id_creator=creator_id
    )
    db_event = events.create_event(db=db, event=event_with_creator_id)
    return db_event


@router.get("/{event_id}", response_model=EventSchemaWithEventId)
def read_event(event_id: str, db: Session = Depends(get_db)):
    return events.get_event(db=db, event_id=event_id)


@router.put("/", response_model=EventSchemaWithEventId)
def update_event(
    event: EventSchemaWithEventId,
    modifier_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    event_updated = ModifyEventSchema(**event.model_dump(), id_modifier=modifier_id)
    return events.update_event(db=db, event_updated=event_updated)


@router.delete("/{event_id}", response_model=EventSchema)
def delete_event(event_id: str, db: Session = Depends(get_db)):
    return events.delete_event(db=db, event_id=event_id)
