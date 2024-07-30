from typing import Annotated
from fastapi import Depends, HTTPException, Header
from app.authorization.user_id_dep import UserDep
from app.database.models.user import UserRole
from app.database.session_dep import SessionDep
from app.database.models.event import EventModel
from app.database.models.event import EventStatus


# TODO: ver si se puede hacer mas bonito el chequeo de admin.
# El problema con esta dependencia es que se tiene que hacer solamente
# si se pide determinado status distinto de STARTED.
class GetEventQueryChecker:
    async def __call__(
        self,
        db: SessionDep,
        role: UserDep,
        status: EventStatus | None = None,
        X_User_Id: str | None = Header(default=None),
    ):
        if (status != EventStatus.STARTED and role != UserRole.ADMIN):
            raise HTTPException(status_code=400)  # TODO: move to service.
        return status


get_events_query_checker = GetEventQueryChecker()
GetEventsQuerysDep = Annotated[EventModel, Depends(get_events_query_checker)]
