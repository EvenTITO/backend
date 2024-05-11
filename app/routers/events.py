from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud import events
from app.schemas.events import EventSchema

from fastapi import APIRouter, HTTPException, Depends


router = APIRouter(
    prefix="/events",
    tags=['Events']
)


@router.post("/", response_model=EventSchema)
def create_event(event: EventSchema, db: Session = Depends(get_db)):
    try:
        event_created = events.create_event(db=db, event=event)

        return event_created
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
