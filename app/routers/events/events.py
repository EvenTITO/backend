from typing import List

from fastapi import APIRouter, Depends, Query

from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.user_id_dep import UserDep, verify_user_exists
from app.database.models.event import EventStatus
from app.routers.events.administration import events_admin_router
from app.routers.events.configuration.configuration import events_configuration_router
from app.routers.events.inscriptions.inscriptions import inscriptions_events_router
from app.routers.events.media import events_media_router
from app.routers.events.members.chairs import event_chairs_router
from app.routers.events.members.members import event_members_router
from app.routers.events.members.organizers import event_organizers_router
from app.routers.works.submissions import works_submissions_router, submissions_router
from app.routers.works.works import works_router
from app.schemas.events.create_event import CreateEventSchema
from app.schemas.events.public_event import PublicEventSchema
from app.schemas.events.public_event_with_roles import PublicEventWithRolesSchema
from app.services.events.events_service_dep import EventsServiceDep

events_router = APIRouter(prefix="/events")
events_router.include_router(events_media_router)
events_router.include_router(events_configuration_router)
events_router.include_router(events_admin_router)
events_router.include_router(event_members_router)
events_router.include_router(event_organizers_router)
events_router.include_router(event_chairs_router)
events_router.include_router(works_router)
events_router.include_router(inscriptions_events_router)
events_router.include_router(works_submissions_router)
events_router.include_router(submissions_router)


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


@events_router.get(path="/", response_model=List[PublicEventSchema], tags=["Events: General"])
async def read_all_events(
        user_role: UserDep,
        events_service: EventsServiceDep,
        status: EventStatus | None = None,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
        search: str | None = None,
):
    return await events_service.get_all_events(offset, limit, status, search, user_role)


@events_router.post("", status_code=201, response_model=str, tags=["Events: General"])
async def create_event(
        event: CreateEventSchema,
        user_role: UserDep,
        caller_id: CallerIdDep,
        events_service: EventsServiceDep
):
    return await events_service.create(event, caller_id, user_role)


@events_router.get("/{event_id}/public", response_model=PublicEventWithRolesSchema, tags=["Events: General"])
async def read_event_general(events_service: EventsServiceDep, caller_id: CallerIdDep, event_id: str):
    return await events_service.get_public_event(caller_id, event_id)
