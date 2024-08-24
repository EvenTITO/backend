from fastapi import APIRouter, Depends

from app.authorization.organizer_or_admin_dep import verify_is_organizer_or_admin
from app.services.events.events_administration_service_dep import EventsAdministrationServiceDep
from ...authorization.user_id_dep import UserDep
from ...schemas.events.event_status import EventStatusSchema

events_admin_router = APIRouter(prefix="/{event_id}", tags=["Events: Administration"])


@events_admin_router.patch(
    "/status",
    status_code=204,
    response_model=None,
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def change_event_status(
        service: EventsAdministrationServiceDep,
        event_id: str,
        status_modification: EventStatusSchema,
        user_role: UserDep
):
    await service.update_status(event_id, status_modification, user_role)
