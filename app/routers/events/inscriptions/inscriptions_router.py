from fastapi import APIRouter, Depends, Query
from typing import List
from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.user_id_dep import verify_user_exists
from app.authorization.same_user_or_admin_dep import SameUserOrAdminDep
from ....schemas.inscriptions.schemas import (
    InscriptionReplySchema
)
from app.database.session_dep import SessionDep
from app.repository import inscriptions_crud
from app.routers.users.users import users_router
from app.routers.events.events import events_router
from app.inscriptions import validations


inscriptions_PREFIX = '/inscriptions'

inscriptions_events_router = APIRouter(
    prefix=events_router.prefix + "/{event_id}" + inscriptions_PREFIX,
    tags=["Event inscriptions"]
)

@inscriptions_events_router.post(
    "",
    status_code=201,
    dependencies=[Depends(verify_user_exists)]
)
async def create_inscription(
    event_id: str,
    caller_id: CallerIdDep,
    db: SessionDep
) -> str:
    await validations.validate_inscription_not_exists(
        db, caller_id, event_id
    )
    new_entry = await inscriptions_crud.inscribe_user_to_event(
        db, event_id, caller_id
    )
    return new_entry.inscriptor_id


@inscriptions_events_router.get(
    "", response_model=List[InscriptionReplySchema]
)
async def read_event_inscriptions(event_id: str, db: SessionDep):
    return await inscriptions_crud.get_event_inscriptions(db, event_id)
