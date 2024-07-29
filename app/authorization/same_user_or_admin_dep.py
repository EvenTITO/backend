from typing import Annotated
from app.database.models.user import UserModel, UserRole
from fastapi import HTTPException, Depends
from app.authorization.caller_user_dep import CallerUserDep


class SameUserOrAdmin:
    async def __call__(self, user_id: str, caller_user: CallerUserDep):
        if user_id != caller_user.id and caller_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403)

        return caller_user


same_user_or_admin = SameUserOrAdmin()
SameUserOrAdminDep = Annotated[UserModel, Depends(same_user_or_admin)]
