from fastapi import APIRouter, Depends
from app.authorization.organizer_or_admin_dep import OrganizerOrAdminDep, verify_is_organizer
from app.services.events.events_administration_service_dep import EventsAdministrationServiceDep
from ...schemas.events.event_status import EventStatusSchema


events_admin_router = APIRouter(prefix="/{event_id}", tags=["Events: Administration"])


@events_admin_router.patch(
    "/status",
    status_code=204,
    response_model=None,
    dependencies=[Depends(verify_is_organizer)]
)
async def change_event_status(
    service: EventsAdministrationServiceDep,
    event_id: str,
    status_modification: EventStatusSchema,
    user_role: OrganizerOrAdminDep
):
    await service.update_status(event_id, status_modification, user_role)


@events_admin_router.patch(
    "/publish",
    status_code=204,
    response_model=None,
    dependencies=[Depends(verify_is_organizer)]
)
async def publish_event(
    service: EventsAdministrationServiceDep,
    event_id: str,
    user_role: OrganizerOrAdminDep
):
    await service.publish_event(event_id, user_role)
