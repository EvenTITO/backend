from typing import List
from app.users.dependencies import CallerUserDep, SameUserDep, SameUserOrAdminDep
from .schemas import (
    InscriptionReplySchema, InscriptorRequestSchema
)
from app.database.dependencies import SessionDep
from app.inscriptions import crud
from fastapi import APIRouter, Query
from app.users.router import users_router
from app.events.router import events_router
from app.inscriptions import validations

inscriptions_PREFIX = '/inscriptions'

inscriptions_events_router = APIRouter(
    prefix=events_router.prefix + "/{event_id}" + inscriptions_PREFIX,
    tags=["Event inscriptions"]
)

inscriptions_users_router = APIRouter(
    prefix=users_router.prefix + "/{user_id}" + inscriptions_PREFIX,
    tags=["User inscriptions"]
)


@inscriptions_events_router.post(
    "",
    status_code=201
)
async def create_inscription(
    inscription: InscriptorRequestSchema,
    event_id: str,
    caller_user: CallerUserDep,
    db: SessionDep
) -> str:
    await validations.validate_inscription_not_exists(
        db, caller_user.id, event_id
    )
    new_entry = await crud.inscribe_user_to_event(
        db, event_id, inscription.id_inscriptor
    )
    return new_entry.id_inscriptor


@inscriptions_events_router.get(
    "", response_model=List[InscriptionReplySchema]
)
async def read_event_inscriptions(event_id: str, db: SessionDep):
    return await crud.get_event_inscriptions(db, event_id)


@inscriptions_users_router.get(
    "", response_model=List[InscriptionReplySchema]
)
async def read_user_inscriptions(
    user_id: str,
    _: SameUserOrAdminDep,
    db: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return await crud.read_user_inscriptions(db, user_id, offset, limit)
