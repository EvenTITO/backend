from typing import Annotated
from app.repository.users_crud import get_user_by_id
from app.users.exceptions import UserNotFound
from app.models.user import UserModel, UserRole
from fastapi import HTTPException, Depends
from app.utils.dependencies import CallerIdDep
from app.database.dependencies import SessionDep


class CallerUser:
    async def __call__(
        self,
        caller_id: CallerIdDep,
        db: SessionDep
    ) -> UserModel:
        user = await get_user_by_id(db, caller_id)
        if not user:
            raise UserNotFound(caller_id)
        return user


caller_user_checker = CallerUser()
CallerUserDep = Annotated[UserModel, Depends(caller_user_checker)]


class AdminUser:
    async def __call__(self, caller_user: CallerUserDep) -> UserModel:
        if caller_user.role == UserRole.ADMIN:
            return caller_user
        else:
            raise HTTPException(status_code=403)


admin_user_checker = AdminUser()
AdminDep = Annotated[UserModel, Depends(admin_user_checker)]


class SameUserOrAdmin:
    async def __call__(self, user_id: str, caller_user: CallerUserDep):
        if user_id != caller_user.id and caller_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403)

        return caller_user


same_user_or_admin = SameUserOrAdmin()
SameUserOrAdminDep = Annotated[UserModel, Depends(same_user_or_admin)]


class SameUser:
    async def __call__(self, user_id: str, caller_user: CallerUserDep):
        if user_id != caller_user.id:
            raise HTTPException(status_code=403)
        return caller_user


same_user = SameUser()
SameUserDep = Annotated[UserModel, Depends(same_user)]


class CreatorOrAdminUser:
    async def __call__(self, cu: CallerUserDep) -> UserModel:
        if cu.role == UserRole.EVENT_CREATOR or cu.role == UserRole.ADMIN:
            return cu
        else:
            raise HTTPException(status_code=403)


creator_or_admin_user = CreatorOrAdminUser()
CreatorOrAdminUserDep = Annotated[UserModel, Depends(creator_or_admin_user)]
