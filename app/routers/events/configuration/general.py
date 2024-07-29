from fastapi import APIRouter
from app.repository import events_crud
from app.database.session_dep import SessionDep
from app.organizers.dependencies import EventOrganizerDep
from app.events.utils import get_event
from app.schemas.events.configuration_general import ConfigurationGeneralEventSchema


general_configuration_router = APIRouter(prefix="/general")


@general_configuration_router.put("", status_code=204, response_model=None)
async def update_general_event(
    _: EventOrganizerDep,
    event_id: str,
    event_modification: ConfigurationGeneralEventSchema,
    db: SessionDep
):
    current_event = await get_event(db, event_id)
    await events_crud.update_event(db, current_event, event_modification)
