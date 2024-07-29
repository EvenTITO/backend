from fastapi import APIRouter
from app.database.session_dep import SessionDep
from app.organizers.dependencies import EventOrganizerDep
from app.events.utils import get_event
from app.schemas.events.configuration import EventConfigurationSchema
from app.routers.events.configuration.dates import dates_configuration_router
from app.routers.events.configuration.general import general_configuration_router
from app.routers.events.configuration.pricing import pricing_configuration_router
from app.routers.events.configuration.review_skeleton import review_skeleton_configuration_router


events_configuration_router = APIRouter(prefix="/{event_id}/configuration", tags=["Events: Configuration"])

events_configuration_router.include_router(dates_configuration_router)
events_configuration_router.include_router(general_configuration_router)
events_configuration_router.include_router(pricing_configuration_router)
events_configuration_router.include_router(review_skeleton_configuration_router)


@events_configuration_router.get("")
async def get_event_configuration(
    _: EventOrganizerDep,
    event_id: str,
    db: SessionDep
) -> EventConfigurationSchema:
    event = await get_event(db, event_id)
    return event
