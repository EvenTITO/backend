from typing import Annotated
from app.models.user import UserModel, UserRole
from fastapi import HTTPException, Depends
from app.dependencies.caller_user_dep import CallerUserDep


class AdminUser:
    async def __call__(self, caller_user: CallerUserDep) -> UserModel:
        if caller_user.role == UserRole.ADMIN:
            return caller_user
        else:
            raise HTTPException(status_code=403)


admin_user_checker = AdminUser()
AdminDep = Annotated[UserModel, Depends(admin_user_checker)]
