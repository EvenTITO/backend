from typing import List
from fastapi import APIRouter, Query
from app.database.dependencies import SessionDep
from app.events.dependencies import GetEventsQuerysDep
from app.users.dependencies import CallerUserDep
from app.organizers.dependencies import EventOrganizerDep
from app.events import crud, validations
from .utils import get_event
from .schemas import (
    EventSchema,
    EventSchemaWithEventId,
    ModifyEventStatusSchema,
    EventProfileWithIdSchema
)

from .model import EventStatus


events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.get("/", response_model=List[EventSchemaWithEventId])
async def read_all_events(
    db: SessionDep,
    status_query: GetEventsQuerysDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str | None = None
):
    print('El valor de la query es')
    print(status_query)
    return await crud.get_all_events(
        db=db,
        offset=offset,
        limit=limit,
        status=status_query,
        title_search=search
    )


@events_router.get("/public", response_model=List[EventSchemaWithEventId])
async def read_all_events_public(
    db: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    title_search: str | None = None
):
    return await crud.get_all_events(
        db=db,
        offset=offset,
        limit=limit,
        status=EventStatus.STARTED,
        title_search=title_search
    )

# 2- agregar endpoint GET /events/<eventid>/profile que te diga
# tu informacion con respecto a ese evento: si estoy inscripto,
# si soy organizador, etc. >>> Me fijo como seria el response y te digo
# TODO: Hay que machear los eventos para el User logeado


@events_router.get("/{event_id}/profile",
                   response_model=EventProfileWithIdSchema)
async def read_event_profile(event_id: str, db: SessionDep):
    print('Estoy en /event_id/profile ...')
    return await get_event(db, event_id)


@events_router.post("", status_code=201, response_model=str)
async def create_event(
    event: EventSchema,
    caller_user: CallerUserDep,
    db: SessionDep
):
    await validations.validate_event_not_exists(db, event)
    event_created = await crud.create_event(
        db=db,
        event=event,
        id_creator=caller_user.id
    )
    return event_created.id


@events_router.get("/{event_id}", response_model=EventSchemaWithEventId)
async def read_event(event_id: str, db: SessionDep):
    return await get_event(db, event_id)


@events_router.put("/{event_id}", status_code=204, response_model=None)
async def update_event(
    _: EventOrganizerDep,
    event_id: str,
    event_modification: EventSchema,
    db: SessionDep
):
    current_event = await get_event(db, event_id)
    await validations.validate_update(db, current_event, event_modification)
    await crud.update_event(db, current_event, event_modification)


@events_router.patch(
    "/{event_id}/status",
    status_code=204,
    response_model=None
)
async def change_event_status(
    caller: CallerUserDep,
    event_id: str,
    status_modification: ModifyEventStatusSchema,
    db: SessionDep
):
    event = await get_event(db, event_id)
    await validations.validate_status_change(
        db, caller, event, status_modification
    )
    await crud.update_status(db, event, status_modification.status)

# @events_router.delete("/{event_id}", status_code=204, response_model=None)
# async def delete_event(event_id: str, db: SessionDep):
#     crud.delete_event(db=db, event_id=event_id)
