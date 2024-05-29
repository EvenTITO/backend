from typing import Annotated
from fastapi import HTTPException, Depends
from app.users.dependencies import CallerUserDep
from app.events.utils import get_event
from app.organizers import crud
from app.events.model import EventModel
from app.database.dependencies import SessionDep


class EventOrganizerChecker:
    async def __call__(
        self,
        event_id: str,
        caller_user: CallerUserDep,
        db: SessionDep
    ):
        event = await get_event(db, event_id)
        if not await crud.is_organizer(db, event_id, caller_user.id):
            raise HTTPException(status_code=403)
        return event


event_organizer_dep = EventOrganizerChecker()
EventOrganizerDep = Annotated[EventModel, Depends(event_organizer_dep)]