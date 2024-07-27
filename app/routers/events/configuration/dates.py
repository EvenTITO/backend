from fastapi import APIRouter
from app.repository import events_crud
from app.database.dependencies import SessionDep
from app.organizers.dependencies import EventOrganizerDep
from app.events.utils import get_event
from app.schemas.events.dates import DatesCompleteSchema

dates_configuration_router = APIRouter(prefix="/dates")


@dates_configuration_router.put("", status_code=204, response_model=None)
async def update_dates_event(
    _: EventOrganizerDep,
    event_id: str,
    dates_modification: DatesCompleteSchema,
    db: SessionDep
):
    current_event = await get_event(db, event_id)
    await events_crud.update_dates(db, current_event, dates_modification)
