from fastapi import APIRouter, Depends
from typing import List
from app.authorization.user_id_dep import verify_user_exists
from app.services.event_inscriptions.event_inscriptions_service_dep import EventInscriptionsServiceDep
from app.schemas.inscriptions.schemas import InscriptionReplySchema
from app.authorization.organizer_or_admin_dep import verify_is_organizer


inscriptions_events_router = APIRouter(
    prefix="/{event_id}/inscriptions",
    tags=["Event inscriptions"]
)


@inscriptions_events_router.post(
    path="",
    status_code=201,
    dependencies=[Depends(verify_user_exists)]
)
async def create_inscription(
    inscriptions_service: EventInscriptionsServiceDep,
) -> str:
    return await inscriptions_service.inscribe_user_to_event()


@inscriptions_events_router.get(
    path="",
    response_model=List[InscriptionReplySchema],
    dependencies=[Depends(verify_is_organizer)]
)
async def read_event_inscriptions(inscriptions_service: EventInscriptionsServiceDep):
    return await inscriptions_service.get_event_inscriptions()
