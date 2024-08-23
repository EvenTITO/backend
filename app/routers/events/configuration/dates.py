from fastapi import APIRouter, Depends
from app.schemas.events.dates import DatesCompleteSchema
from app.services.events.events_configuration_service_dep import EventsConfigurationServiceDep
from app.authorization.organizer_or_admin_dep import verify_is_organizer_or_admin


dates_configuration_router = APIRouter(prefix="/dates")


@dates_configuration_router.put("", status_code=204, response_model=None, dependencies=[Depends(verify_is_organizer_or_admin)])
async def update_dates_event(
    dates_modification: DatesCompleteSchema,
    events_configuration_service: EventsConfigurationServiceDep,
):
    await events_configuration_service.update_dates(dates_modification)
