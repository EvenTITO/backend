from sqlalchemy.orm import Session
from app.utils.dependencies import SessionDep, CallerIdDep
from app.events import crud
from .schemas import (
    EventSchema, CreateEventSchema,
    ModifyEventSchema, EventSchemaWithEventId,
    PublicEventsSchema
)
from fastapi import APIRouter, Query


events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.post("/", response_model=EventSchemaWithEventId)
def create_event(
    event: EventSchema,
    caller_id: CallerIdDep,
    db: SessionDep
):
    event_with_creator_id = CreateEventSchema(
        **event.model_dump(),
        id_creator=caller_id
    )
    db_event = crud.create_event(db=db, event=event_with_creator_id)
    return db_event


@events_router.get("/{event_id}", response_model=EventSchemaWithEventId)
def read_event(event_id: str, db: SessionDep):
    return crud.get_event(db=db, event_id=event_id)


@events_router.get("/", response_model=PublicEventsSchema)
def read_all_events(
    db: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return crud.get_all_events(db=db, offset=offset, limit=limit)


@events_router.put("/", response_model=EventSchemaWithEventId)
def update_event(
    event: EventSchemaWithEventId,
    caller_id: CallerIdDep,
    db: SessionDep
):
    event_updated = ModifyEventSchema(
        **event.model_dump(), id_modifier=caller_id
    )
    return crud.update_event(db=db, event_updated=event_updated)


@events_router.delete("/{event_id}", response_model=EventSchema)
def delete_event(event_id: str, db: SessionDep):
    return crud.delete_event(db=db, event_id=event_id)
