from fastapi import APIRouter
from app.repository import events_crud
from app.database.dependencies import SessionDep
from app.organizers.dependencies import EventOrganizerDep
from app.events.utils import get_event
from app.events.schemas import PricingRateSchema

pricing_configuration_router = APIRouter(prefix="/pricing")


@pricing_configuration_router.put("", status_code=204, response_model=None)
async def update_pricing_event(
    _: EventOrganizerDep,
    event_id: str,
    pricing_modification: PricingRateSchema,
    db: SessionDep
):
    current_event = await get_event(db, event_id)
    await events_crud.update_pricing(db, current_event, pricing_modification)
