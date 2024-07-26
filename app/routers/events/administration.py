from fastapi import APIRouter
from app.repository import events_crud
from app.database.dependencies import SessionDep
from app.users.dependencies import CallerUserDep
from app.events import validations
from ...events.utils import get_event
from ...schemas.schemas import EventStatusSchema


events_admin_router = APIRouter(prefix="/{event_id}", tags=["Events: Administration"])


@events_admin_router.patch(
    "/status",
    status_code=204,
    response_model=None
)
async def change_event_status(
        caller: CallerUserDep,
        event_id: str,
        status_modification: EventStatusSchema,
        db: SessionDep
):
    event = await get_event(db, event_id)
    await validations.validate_status_change(
        db, caller, event, status_modification
    )
    await events_crud.update_status(db, event, status_modification.status)
