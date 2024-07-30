from fastapi import APIRouter, Depends
from app.authorization.organizer_or_admin_dep import OrganizerOrAdminDep, organizer_or_admin_checker
from app.services.events.events_service_dep import EventsServiceDep
from ...schemas.events.event_status import EventStatusSchema


events_admin_router = APIRouter(prefix="/{event_id}", tags=["Events: Administration"])


@events_admin_router.patch(
    "/status",
    status_code=204,
    response_model=None,
    dependencies=[Depends(organizer_or_admin_checker)]
)
async def change_event_status(
    service: EventsServiceDep,
    event_id: str,
    status_modification: EventStatusSchema,
    user_role: OrganizerOrAdminDep
):
    await service.modify_status(event_id, status_modification, user_role)
