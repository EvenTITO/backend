from typing import List
from .schemas import (
    SuscriptionSchema, SuscriptionReplySchema, SuscriptorRequestSchema
)
from app.utils.dependencies import CallerIdDep
from app.database.dependencies import SessionDep
from app.suscriptions import crud
from fastapi import APIRouter, Query
from app.users.router import users_router
from app.events.router import events_router
# from app.utils.authorization import (
#     validate_same_user_or_superuser, validate_user_permissions
# )


SUSCRIPTIONS_PREFIX = '/suscriptions'

suscriptions_events_router = APIRouter(
    prefix=events_router.prefix + "/{event_id}" + SUSCRIPTIONS_PREFIX,
    tags=["Event Suscriptions"]
)

suscriptions_users_router = APIRouter(
    prefix=users_router.prefix + "/{user_id}" + SUSCRIPTIONS_PREFIX,
    tags=["User Suscriptions"]
)


@suscriptions_events_router.post(
    "",
    status_code=201
)
def create_suscription(
    suscription: SuscriptorRequestSchema,
    event_id: str,
    caller_id: CallerIdDep,
    db: SessionDep
) -> str:
    validate_user_permissions(suscription.id_suscriptor, caller_id)
    suscription_schema = SuscriptionSchema(
        id_event=event_id, id_suscriptor=suscription.id_suscriptor
    )
    new_entry = crud.suscribe_user_to_event(db, suscription_schema)
    return new_entry.id_suscriptor


@suscriptions_events_router.get(
    "", response_model=List[SuscriptionReplySchema]
)
def read_event_suscriptions(event_id: str, db: SessionDep):
    return crud.read_event_suscriptions(db, event_id)


@suscriptions_users_router.get(
    "", response_model=List[SuscriptionReplySchema]
)
def read_user_suscriptions(
    user_id: str,
    caller_id: CallerIdDep,
    db: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    validate_same_user_or_superuser(db, user_id, caller_id)
    return crud.read_user_suscriptions(db, caller_id, offset, limit)
