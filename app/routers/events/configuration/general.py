from fastapi import APIRouter, Depends

from app.authorization.organizer_or_admin_dep import verify_is_organizer_or_admin
from app.schemas.events.configuration_general import ConfigurationGeneralEventSchema
from app.schemas.events.schemas import DynamicTracksEventSchema
from app.services.events.events_configuration_service_dep import EventsConfigurationServiceDep

general_configuration_router = APIRouter(prefix="/general")


@general_configuration_router.put(
    path="", status_code=204,
    response_model=None,
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def update_general_event(
        event_modification: ConfigurationGeneralEventSchema,
        events_configuration_service: EventsConfigurationServiceDep,
) -> None:
    await events_configuration_service.update_general(event_modification)


@general_configuration_router.put(
    path="/tracks",
    status_code=204,
    response_model=None,
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def update_event_tracks(
        tracks_schema: DynamicTracksEventSchema,
        events_configuration_service: EventsConfigurationServiceDep,
):
    await events_configuration_service.update_tracks(tracks_schema)
