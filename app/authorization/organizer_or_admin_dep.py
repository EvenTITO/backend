from fastapi import Depends, HTTPException
from typing import Annotated, Union

from app.database.models.user import UserRole
from app.database.session_dep import SessionDep
from app.repository import organizers_crud
from app.schemas.events.schemas import EventRol
from app.authorization.caller_id_dep import CallerIdDep
from app.services.users.users_service_dep import UsersServiceDep


class OrganizerOrAdminChecker:
    async def __call__(
        self,
        caller_id: CallerIdDep,
        event_id: str,
        users_servide: UsersServiceDep,
        db: SessionDep
    ) -> Union[EventRol, UserRole]:
        role = await users_servide.get_role()
        if role == UserRole.ADMIN:
            return UserRole.ADMIN
        if not await organizers_crud.is_organizer(
            db,
            event_id,
            caller_id
        ):
            raise HTTPException(status_code=403)
        return EventRol.ORGANIZER


organizer_or_admin_checker = OrganizerOrAdminChecker()
OrganizerOrAdminDep = Annotated[str, Depends(organizer_or_admin_checker)]
