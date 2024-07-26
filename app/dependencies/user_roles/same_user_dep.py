from typing import Annotated
from app.models.user import UserModel
from fastapi import HTTPException, Depends
from app.dependencies.user_roles.caller_user_dep import CallerUserDep


class SameUser:
    async def __call__(self, user_id: str, caller_user: CallerUserDep):
        if user_id != caller_user.id:
            raise HTTPException(status_code=403)
        return caller_user


same_user = SameUser()
SameUserDep = Annotated[UserModel, Depends(same_user)]
