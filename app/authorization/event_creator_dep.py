from typing import Annotated
from app.database.models.user import UserModel, UserRole
from fastapi import HTTPException, Depends
from app.authorization.caller_user_dep import CallerUserDep


class CreatorOrAdminUser:
    async def __call__(self, cu: CallerUserDep) -> UserModel:
        if cu.role == UserRole.EVENT_CREATOR or cu.role == UserRole.ADMIN:
            return cu
        else:
            raise HTTPException(status_code=403)


creator_or_admin_user = CreatorOrAdminUser()
EventCreatorDep = Annotated[UserModel, Depends(creator_or_admin_user)]
