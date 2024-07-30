from typing import Annotated
from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.user_id_dep import UserDep
from app.database.models.user import UserRole
from fastapi import HTTPException, Depends


class SameUserOrAdmin:
    async def __call__(self, user_id: str, caller_user_role: UserDep, caller_id: CallerIdDep):
        if user_id != caller_id and caller_user_role != UserRole.ADMIN:
            raise HTTPException(status_code=403)


same_user_or_admin = SameUserOrAdmin()
SameUserOrAdminDep = Annotated[None, Depends(same_user_or_admin)]
