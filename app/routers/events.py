from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud import events
from app.schemas.events import EventSchema, CreateEventSchema, ReplyEventSchema
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/events",
    tags=['Events']
)


@router.post("/", response_model=ReplyEventSchema)
def create_event(event: CreateEventSchema, db: Session = Depends(get_db)):
    return events.create_event(db=db, event=event)


@router.get("/{event_id}", response_model=EventSchema)
def read_event(event_id: str, db: Session = Depends(get_db)):
    return events.get_event(db=db, event_id=event_id)


@router.put("/", response_model=EventSchema)
def update_event(event: EventSchema, db: Session = Depends(get_db)):
    return events.update_event(db=db, event_updated=event)


@router.delete("/{event_id}", response_model=EventSchema)
def delete_event(event_id: str, db: Session = Depends(get_db)):
    return events.delete_event(db=db, event_id=event_id)
