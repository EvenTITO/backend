from fastapi import APIRouter, Depends
from typing import List
from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.user_id_dep import verify_user_exists
from app.services.event_inscriptions.event_inscriptions_service_dep import EventInscriptionsServiceDep
from ....schemas.inscriptions.schemas import (
    InscriptionReplySchema
)
from app.database.session_dep import SessionDep
from app.repository import inscriptions_crud
from app.inscriptions import validations


inscriptions_PREFIX = '/'

inscriptions_events_router = APIRouter(
    prefix="/{event_id}/inscriptions",
    tags=["Event inscriptions"]
)


@inscriptions_events_router.post(
    "",
    status_code=201,
    dependencies=[Depends(verify_user_exists)]
)
async def create_inscription(
    inscriptions_service: EventInscriptionsServiceDep,
) -> str:
    return await inscriptions_service.inscribe_user_to_event()


@inscriptions_events_router.get(
    "", response_model=List[InscriptionReplySchema]
)
async def read_event_inscriptions(event_id: str, db: SessionDep):
    return await inscriptions_crud.get_event_inscriptions(db, event_id)
