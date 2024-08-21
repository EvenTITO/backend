from fastapi import Depends, HTTPException
from typing import Annotated, Union

from app.authorization.user_id_dep import UserDep
from app.database.models.user import UserRole
from app.schemas.events.schemas import EventRole
from app.authorization.caller_id_dep import CallerIdDep
from app.services.event_organizers.event_organizers_service_dep import EventOrganizersServiceDep


class OrganizerOrAdminChecker:
    async def __call__(
        self,
        caller_id: CallerIdDep,
        event_id: str,
        organizers_service: EventOrganizersServiceDep,
        role: UserDep,
    ) -> Union[EventRole, UserRole]:
        if role == UserRole.ADMIN:
            return UserRole.ADMIN
        if await organizers_service.is_organizer(event_id, caller_id):
            return EventRole.ORGANIZER
        raise HTTPException(status_code=403)


verify_is_organizer = OrganizerOrAdminChecker()
OrganizerOrAdminDep = Annotated[str, Depends(verify_is_organizer)]
