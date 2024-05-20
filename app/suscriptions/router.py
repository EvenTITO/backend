from .schemas import (
    GetSuscriptionReplySchema,
    SuscriptionReplySchema,
    SuscriptionSchema
)
from sqlalchemy.orm import Session
from app.utils.dependencies import SessionDep, CallerIdDep
from app.suscriptions import crud
from fastapi import APIRouter


suscriptions_router = APIRouter(prefix="/suscriptions", tags=["Suscriptions"])


@suscriptions_router.post(
    "/{event_id}/",
    response_model=SuscriptionReplySchema
)
def create_suscription(
    event_id: str,
    caller_id: CallerIdDep,
    db: SessionDep
):
    suscription_schema = SuscriptionSchema(
        id_event=event_id, id_suscriptor=caller_id
    )
    return crud.suscribe_user_to_event(db, suscription_schema)


@suscriptions_router.get(
    "/events/{event_id}/", response_model=GetSuscriptionReplySchema
)
def read_event_suscriptions(event_id: str, db: SessionDep):
    return crud.read_event_suscriptions(db, event_id)


@suscriptions_router.get(
    "/users/", response_model=GetSuscriptionReplySchema
)
def read_user_suscriptions(
    caller_id: CallerIdDep,
    db: SessionDep
):
    return crud.read_user_suscriptions(db, caller_id)