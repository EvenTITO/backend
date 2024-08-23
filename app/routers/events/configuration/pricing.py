from fastapi import APIRouter, Depends
from app.schemas.events.schemas import PricingSchema
from app.services.events.events_configuration_service_dep import EventsConfigurationServiceDep
from app.authorization.organizer_or_admin_dep import verify_is_organizer_or_admin

pricing_configuration_router = APIRouter(prefix="/pricing")


@pricing_configuration_router.put("", status_code=204, response_model=None, dependencies=[Depends(verify_is_organizer_or_admin)])
async def update_pricing_event(
    pricing_modification: PricingSchema,
    events_configuration_service: EventsConfigurationServiceDep,
):
    await events_configuration_service.update_pricing(pricing_modification)
