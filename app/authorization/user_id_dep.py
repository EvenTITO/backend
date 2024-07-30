from fastapi import Depends
from typing import Annotated

from app.services.users.exceptions import UserNotFound
from app.authorization.caller_id_dep import CallerIdDep
from app.services.users.users_service_dep import UsersServiceDep


class UserId:
    async def __call__(
        self,
        caller_id: CallerIdDep,
        users_servide: UsersServiceDep,
    ) -> str:
        exists = await users_servide.exists(caller_id)
        if not exists:
            raise UserNotFound(caller_id)
        return caller_id


user_id_exists_checker = UserId()
UserIdDep = Annotated[str, Depends(user_id_exists_checker)]
