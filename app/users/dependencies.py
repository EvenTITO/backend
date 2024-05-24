from typing import Annotated
from app.users.model import UserModel, UserRole
from fastapi import HTTPException, Depends
from app.utils.dependencies import CallerUserDep


class SameUserOrAdmin:
    def __call__(self, user_id: str, caller_user: CallerUserDep):
        if user_id != caller_user.id and caller_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403)

        return caller_user


same_user_or_admin = SameUserOrAdmin()
SameUserOrAdminDep = Annotated[UserModel, Depends(same_user_or_admin)]


class SameUser:
    def __call__(self, user_id: str, caller_user: CallerUserDep):
        if user_id != caller_user.id:
            raise HTTPException(status_code=403)
        return caller_user


same_user = SameUser()
SameUserDep = Annotated[UserModel, Depends(same_user)]
