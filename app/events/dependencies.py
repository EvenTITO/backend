from typing import Annotated
from fastapi import Depends, Header
from app.database.session_dep import SessionDep
from app.database.models.event import EventModel
from app.database.models.event import EventStatus
from app.authorization.admin_user_dep import admin_user_checker
from app.authorization.caller_user_dep import verify_user_exists
from app.authorization.caller_id_dep import get_user_id
from app.services.users.users_service_dep import UsersServiceDep


# TODO: ver si se puede hacer mas bonito el chequeo de admin.
# El problema con esta dependencia es que se tiene que hacer solamente
# si se pide determinado status distinto de STARTED.
class GetEventQueryChecker:
    async def __call__(
        self,
        db: SessionDep,
        users_service: UsersServiceDep,
        status: EventStatus | None = None,
        X_User_Id: str | None = Header(default=None),
    ):
        if (status != EventStatus.STARTED):
            await admin_user_checker(
                users_service
            )
        return status


get_events_query_checker = GetEventQueryChecker()
GetEventsQuerysDep = Annotated[EventModel, Depends(get_events_query_checker)]
