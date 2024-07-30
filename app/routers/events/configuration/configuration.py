from fastapi import APIRouter, Depends
from app.schemas.events.configuration import EventConfigurationSchema
from app.routers.events.configuration.dates import dates_configuration_router
from app.routers.events.configuration.general import general_configuration_router
from app.routers.events.configuration.pricing import pricing_configuration_router
from app.routers.events.configuration.review_skeleton import review_skeleton_configuration_router
from app.authorization.organizer_or_admin_dep import verify_is_organizer
from app.services.events.events_configuration_service_dep import EventsConfigurationServiceDep

events_configuration_router = APIRouter(prefix="/{event_id}/configuration", tags=["Events: Configuration"])

events_configuration_router.include_router(dates_configuration_router)
events_configuration_router.include_router(general_configuration_router)
events_configuration_router.include_router(pricing_configuration_router)
events_configuration_router.include_router(review_skeleton_configuration_router)


@events_configuration_router.get("", dependencies=[Depends(verify_is_organizer)])
async def get_event_configuration(
    events_configuration_service: EventsConfigurationServiceDep
) -> EventConfigurationSchema:
    event = await events_configuration_service.get_configuration()
    return event
