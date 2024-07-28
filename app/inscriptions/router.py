from fastapi import APIRouter, Query
from typing import List
from app.dependencies.user_roles.caller_user_dep import CallerUserDep
from app.dependencies.user_roles.same_user_or_admin_dep import SameUserOrAdminDep
from .schemas import (
    InscriptionReplySchema
)
from app.dependencies.database.session_dep import SessionDep
from app.repository import inscriptions_crud
from app.routers.users.users import users_router
from app.routers.events.events import events_router
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
    event_id: str,
    caller_user: CallerUserDep,
    db: SessionDep
) -> str:
    await validations.validate_inscription_not_exists(
        db, caller_user.id, event_id
    )
    new_entry = await inscriptions_crud.inscribe_user_to_event(
        db, event_id, caller_user.id
    )
    return new_entry.id_inscriptor


@inscriptions_events_router.get(
    "", response_model=List[InscriptionReplySchema]
)
async def read_event_inscriptions(event_id: str, db: SessionDep):
    return await inscriptions_crud.get_event_inscriptions(db, event_id)


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
    return await inscriptions_crud.read_user_inscriptions(
        db,
        user_id,
        offset,
        limit
    )
