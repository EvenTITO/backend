from typing import Annotated
from fastapi import Depends, Header
from app.database.dependencies import SessionDep
from app.models.event import EventModel
from app.models.event import EventStatus
from app.dependencies.admin_user_dep import admin_user_checker
from app.dependencies.caller_user_dep import caller_user_checker
from app.utils.dependencies import get_user_id


# TODO: ver si se puede hacer mas bonito el chequeo de admin.
# El problema con esta dependencia es que se tiene que hacer solamente
# si se pide determinado status distinto de STARTED.
class GetEventQueryChecker:
    async def __call__(
        self,
        db: SessionDep,
        status: EventStatus | None = None,
        X_User_Id: str | None = Header(default=None)
    ):
        print('no deberia ser admin')
        if (status != EventStatus.STARTED):
            print('deberia ser admin')
            await admin_user_checker(
                await caller_user_checker(
                    caller_id=await get_user_id(X_User_Id),
                    db=db
                )
            )
            print('pasa el chequeo')
        return status


get_events_query_checker = GetEventQueryChecker()
GetEventsQuerysDep = Annotated[EventModel, Depends(get_events_query_checker)]
