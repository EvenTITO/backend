from app.utils.dependencies import (
    SessionDep,
    CallerIdDep,
    CreatorDep
)
from app.events import crud
from .schemas import (
    EventSchema, CreateEventSchema,
    ModifyEventSchema, EventSchemaWithEventId,
    PublicEventsSchema
)
from fastapi import APIRouter, Query


events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.post("", status_code=201)
def create_event(
    event: EventSchema,
    caller_user: CreatorDep,
    db: SessionDep
) -> str:
    event_with_creator_id = CreateEventSchema(
        **event.model_dump(),
        id_creator=caller_user.id
    )
    event_created = crud.create_event(db=db, event=event_with_creator_id)
    return event_created.id


@events_router.get("/{event_id}", response_model=EventSchemaWithEventId)
def read_event(event_id: str, db: SessionDep):
    return crud.get_event(db=db, event_id=event_id)


@events_router.get("", response_model=PublicEventsSchema)
def read_all_events(
    db: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return crud.get_all_events(db=db, offset=offset, limit=limit)


@events_router.put("/{event_id}", status_code=204)
def update_event(
    event_id: str,
    event: EventSchema,
    caller_id: CallerIdDep,
    db: SessionDep
):
    event_updated = ModifyEventSchema(
        **event.model_dump(),
        id=event_id,
        id_modifier=caller_id
    )
    crud.update_event(db=db, event_updated=event_updated)


@events_router.delete("/{event_id}", status_code=204)
def delete_event(event_id: str, db: SessionDep):
    crud.delete_event(db=db, event_id=event_id)
