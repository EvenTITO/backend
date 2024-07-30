from typing import Annotated
from fastapi import HTTPException, Depends
from app.authorization.user_id_dep import UserIdDep
from app.repository import organizers_crud
from app.database.models.event import EventModel
from app.database.session_dep import SessionDep


class EventOrganizerChecker:
    async def __call__(
        self,
        event_id: str,
        caller_user_id: UserIdDep,
        db: SessionDep
    ):
        if not await organizers_crud.is_organizer(
            db,
            event_id,
            caller_user_id
        ):
            raise HTTPException(status_code=403)


event_organizer_checker = EventOrganizerChecker()
EventOrganizerDep = Annotated[EventModel, Depends(event_organizer_checker)]
