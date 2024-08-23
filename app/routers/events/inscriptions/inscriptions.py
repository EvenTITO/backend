from typing import List

from fastapi import APIRouter, Depends, Query

from app.authorization.organizer_or_admin_dep import verify_is_organizer_or_admin
from app.authorization.user_id_dep import verify_user_exists
from app.schemas.inscriptions.inscription import InscriptionResponseSchema, InscriptionRequestSchema, \
    InscriptionPayResponseSchema
from app.services.event_inscriptions.event_inscriptions_service_dep import EventInscriptionsServiceDep

inscriptions_events_router = APIRouter(
    prefix="/{event_id}/inscriptions",
    tags=["Event: Inscriptions"]
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


@inscriptions_events_router.get(
    path="",
    status_code=200,
    response_model=List[InscriptionResponseSchema],
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def read_event_inscriptions(
        inscriptions_service: EventInscriptionsServiceDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100)
) -> List[InscriptionResponseSchema]:
    return await inscriptions_service.get_event_inscriptions(offset, limit)


@inscriptions_events_router.get(
    path="/my-inscriptions",
    status_code=200,
    response_model=List[InscriptionResponseSchema],
    dependencies=[Depends(verify_user_exists)]
)
async def read_my_inscriptions(
        inscriptions_service: EventInscriptionsServiceDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100)
) -> list[InscriptionResponseSchema]:
    return await inscriptions_service.get_my_event_inscriptions(offset, limit)


@inscriptions_events_router.put(
    path="/{inscription_id}/pay",
    status_code=200,
    dependencies=[Depends(verify_user_exists)]
)
async def submit(inscription_id: str, inscription_service: EventInscriptionsServiceDep) -> InscriptionPayResponseSchema:
    return await inscription_service.pay(inscription_id)
