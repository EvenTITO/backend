from fastapi import APIRouter, Depends

from app.authorization.user_id_dep import verify_user_exists
from app.schemas.inscriptions.inscription import InscriptionResponseSchema, InscriptionRequestSchema
from app.services.event_inscriptions.event_inscriptions_service_dep import EventInscriptionsServiceDep

inscriptions_events_router = APIRouter(
    prefix="/{event_id}/inscriptions",
    tags=["Event inscriptions"]
)


@inscriptions_events_router.post(
    path="",
    status_code=201,
    response_model=InscriptionResponseSchema,
    dependencies=[Depends(verify_user_exists)]
)
async def create_inscription(
        inscription: InscriptionRequestSchema,
        inscriptions_service: EventInscriptionsServiceDep
) -> InscriptionResponseSchema:
    return await inscriptions_service.inscribe_user_to_event(inscription)


"""
@inscriptions_events_router.get(
    path="",
    response_model=List[InscriptionReplySchema],
    dependencies=[Depends(verify_is_organizer)]
)
async def read_event_inscriptions(inscriptions_service: EventInscriptionsServiceDep):
    return await inscriptions_service.get_event_inscriptions()
"""
