from typing import Annotated
from fastapi import HTTPException, Depends
from app.utils.dependencies import CallerUserDep
from app.events.utils import get_event
from app.organizers import crud
from app.events.model import EventModel
from app.utils.dependencies import SessionDep


class EventOrganizerChecker:
    def __call__(
        self,
        event_id: str,
        caller_user: CallerUserDep,
        db: SessionDep
    ):
        event = get_event(db, event_id)
        if not crud.is_organizer(db, event_id, caller_user.id):
            raise HTTPException(status_code=403)
        return event


event_organizer_dep = EventOrganizerChecker()
EventOrganizerDep = Annotated[EventModel, Depends(event_organizer_dep)]
