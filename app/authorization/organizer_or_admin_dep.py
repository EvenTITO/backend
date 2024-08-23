from typing import Annotated

from fastapi import Depends, HTTPException

from app.authorization.admin_user_dep import IsAdminUsrDep
from app.authorization.organizer_dep import IsOrganizerDep


class IsOrganizerOrAdmin:
    async def __call__(self, is_admin: IsAdminUsrDep, is_organizer: IsOrganizerDep) -> bool:
        return is_admin or is_organizer


is_organizer_or_admin = IsOrganizerOrAdmin()
IsOrganizerOrAdminDep = Annotated[bool, Depends(is_organizer_or_admin)]


class VerifyIsOrganizerOrAdmin:
    async def __call__(self, is_event_organizer_or_admin: IsOrganizerOrAdminDep) -> None:
        if not is_event_organizer_or_admin:
            raise HTTPException(status_code=403)


verify_is_organizer_or_admin = VerifyIsOrganizerOrAdmin()
OrganizerOrAdminDep = Annotated[None, Depends(verify_is_organizer_or_admin)]
