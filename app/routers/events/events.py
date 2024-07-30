from fastapi import APIRouter, Depends, Header, Query
from typing import List
from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.user_id_dep import UserDep
from app.database.models.event import EventStatus
from app.database.session_dep import SessionDep
from app.repository.organizers_crud import is_organizer
from app.authorization.user_id_dep import verify_user_exists
from app.events.utils import get_event
from app.schemas.events.public_event import PublicEventSchema
from app.schemas.events.create_event import CreateEventSchema
from app.schemas.events.public_event_with_roles import PublicEventWithRolesSchema
from app.schemas.events.schemas import EventRol
from app.routers.events.media import events_media_router
from app.routers.events.configuration.configuration import events_configuration_router
from app.routers.events.administration import events_admin_router
from app.services.events.events_service_dep import EventsServiceDep

events_router = APIRouter(prefix="/events")
events_router.include_router(events_media_router)
events_router.include_router(events_configuration_router)
events_router.include_router(events_admin_router)


@events_router.get(
    "/my-events",
    response_model=List[PublicEventWithRolesSchema],
    tags=["Events: General"],
    dependencies=[Depends(verify_user_exists)]
)
async def read_my_events(
    caller_id: CallerIdDep,
    events_service: EventsServiceDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return await events_service.get_my_events(caller_id, offset=offset, limit=limit)


@events_router.get("/", response_model=List[PublicEventSchema], tags=["Events: General"])
async def read_all_events(
        db: SessionDep,
        user_role: UserDep,
        events_service: EventsServiceDep,
        status: EventStatus | None = None,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
        search: str | None = None,
):
    return await events_service.get_all_events(offset, limit, status, search, user_role)

    # return await events_crud.get_all_events(
    #     db=db,
    #     offset=offset,
    #     limit=limit,
    #     status=status_query,
    #     title_search=search
    # )


@events_router.post("", status_code=201, response_model=str, tags=["Events: General"])
async def create_event(
    event: CreateEventSchema,
    user_role: UserDep,
    caller_id: CallerIdDep,
    events_service: EventsServiceDep
):
    return await events_service.create(event, caller_id, user_role)
    # TODO: add notifications in events_service.

    # caller_user = await users_service.get_user_by_id(db, caller_id)
    # if event_created.status == EventStatus.WAITING_APPROVAL:
    #     await notifications.request_approve_event(
    #         db, caller_user, event_created
    #     )


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
