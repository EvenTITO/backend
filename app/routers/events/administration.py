from fastapi import APIRouter
from app.services.events.events_admin_dep import EventsAdminServiceDep
from ...schemas.events.event_status import EventStatusSchema


events_admin_router = APIRouter(prefix="/{event_id}", tags=["Events: Administration"])


@events_admin_router.patch(
    "/status",
    status_code=204,
    response_model=None
)
async def change_event_status(
    events_admin_service: EventsAdminServiceDep,
    event_id: str,
    status_modification: EventStatusSchema
):
    await events_admin_service.modify_status(event_id, status_modification)


# THIS CODE IS FOR THE ORGANIZER.

    # event = await get_event(db, event_id)
    # await validations.validate_status_change(
    #     db, caller, event, status_modification
    # )
    # await events_crud.update_status(db, event, status_modification.status)
