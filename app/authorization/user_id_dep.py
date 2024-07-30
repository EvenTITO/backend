from fastapi import Depends
from typing import Annotated

from app.database.models.user import UserRole
from app.exceptions.users_exceptions import UserNotFound
from app.authorization.caller_id_dep import CallerIdDep
from app.services.users.users_service_dep import UsersServiceDep


class UserId:
    async def __call__(
        self,
        caller_id: CallerIdDep,
        users_servide: UsersServiceDep,
    ) -> UserRole:
        user_role = await users_servide.get_role()
        if user_role is None:
            raise UserNotFound(caller_id)
        return user_role


verify_user_exists = UserId()
UserDep = Annotated[UserRole, Depends(verify_user_exists)]
