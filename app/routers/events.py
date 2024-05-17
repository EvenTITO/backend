from app.schemas.suscriptions import (
    GetSuscriptionReplySchema,
    SuscriptionReplySchema,
    SuscriptionSchema,
    UserSuscription
)
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud import events
from app.schemas.events import (
    EventSchema, CreateEventSchema,
    ModifyEventSchema, ReplyEventSchema
)
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=ReplyEventSchema)
def create_event(event: CreateEventSchema, db: Session = Depends(get_db)):
    return events.create_event(db=db, event=event)


@router.get("/{event_id}", response_model=EventSchema)
def read_event(event_id: str, db: Session = Depends(get_db)):
    return events.get_event(db=db, event_id=event_id)


@router.put("/", response_model=EventSchema)
def update_event(event: ModifyEventSchema, db: Session = Depends(get_db)):
    return events.update_event(db=db, event_updated=event)


@router.delete("/{event_id}", response_model=EventSchema)
def delete_event(event_id: str, db: Session = Depends(get_db)):
    return events.delete_event(db=db, event_id=event_id)


@router.post("/{event_id}/suscription", response_model=SuscriptionReplySchema)
def create_suscription(
        event_id: str, user: UserSuscription, db: Session = Depends(get_db)
):
    suscription_schema = SuscriptionSchema(
        id_event=event_id, id_suscriptor=user.id)
    return events.suscribe_user_to_event(db, suscription_schema)


@router.get(
    "/{event_id}/suscriptions", response_model=GetSuscriptionReplySchema
)
def read_suscriptions(event_id: str, db: Session = Depends(get_db)):
    return events.read_event_suscriptions(db, event_id)
