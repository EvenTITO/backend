from app.schemas.suscriptions import (
    GetSuscriptionReplySchema,
    SuscriptionReplySchema,
    SuscriptionSchema
)
from sqlalchemy.orm import Session
from app.utils.dependencies import get_db, get_user_id
from app.crud import suscriptions
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/suscriptions", tags=["Suscriptions"])


@router.post("/{event_id}/", response_model=SuscriptionReplySchema)
def create_suscription(
    event_id: str,
    caller_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    suscription_schema = SuscriptionSchema(
        id_event=event_id, id_suscriptor=caller_id
    )
    return suscriptions.suscribe_user_to_event(db, suscription_schema)


@router.get(
    "/{event_id}/", response_model=GetSuscriptionReplySchema
)
def read_suscriptions(event_id: str, db: Session = Depends(get_db)):
    return suscriptions.read_event_suscriptions(db, event_id)
