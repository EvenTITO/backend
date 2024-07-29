from fastapi import APIRouter, Header, Query
from typing import List
from app.repository import events_crud
from app.database.session_dep import SessionDep
from app.events.dependencies import GetEventsQuerysDep
from app.database.models.event import EventStatus
from app.repository.organizers_crud import is_organizer
from app.authorization.caller_user_dep import CallerUserDep
from app.events import validations
import app.notifications.events as notifications
from app.events.utils import get_event
from app.schemas.events.public_event import PublicEventSchema
from app.schemas.events.create_event import CreateEventSchema
from app.schemas.events.public_event_with_roles import PublicEventWithRolesSchema
from app.schemas.events.schemas import (
    EventRol,
)
from app.routers.events.media import events_media_router
from app.routers.events.configuration.configuration import events_configuration_router
from app.routers.events.administration import events_admin_router

events_router = APIRouter(prefix="/events")
events_router.include_router(events_media_router)
events_router.include_router(events_configuration_router)
events_router.include_router(events_admin_router)


@events_router.get("/my-events", response_model=List[PublicEventWithRolesSchema], tags=["Events: General"])
async def read_my_events(
        db: SessionDep,
        caller_user: CallerUserDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100)  # TODO: use offset & limit.
):
    return await events_crud.get_all_events_for_user(db, caller_user.id)


@events_router.get("/", response_model=List[PublicEventSchema], tags=["Events: General"])
async def read_all_events(
        db: SessionDep,
        status_query: GetEventsQuerysDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
        search: str | None = None
):
    return await events_crud.get_all_events(
        db=db,
        offset=offset,
        limit=limit,
        status=status_query,
        title_search=search
    )


@events_router.post("", status_code=201, response_model=str, tags=["Events: General"])
async def create_event(
        event: CreateEventSchema,
        caller_user: CallerUserDep,
        db: SessionDep
):
    await validations.validate_event_not_exists(db, event)
    event_created = await events_crud.create_event(
        db=db,
        event=event,
        user=caller_user
    )
    if event_created.status == EventStatus.WAITING_APPROVAL:
        await notifications.request_approve_event(
            db, caller_user, event_created
        )
    return event_created.id


@events_router.get("/{event_id}/public", response_model=PublicEventWithRolesSchema, tags=["Events: General"])
async def read_event_general(event_id: str, db: SessionDep,
                             X_User_Id: str = Header(...)):
    event = await get_event(db, event_id)
    event.roles = []
    event = PublicEventWithRolesSchema.model_validate(event)
    if not X_User_Id:
        return event
    if await is_organizer(db, event_id, X_User_Id):
        event.roles.append(EventRol.ORGANIZER)
    return event
