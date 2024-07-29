from fastapi import Depends
from typing import Annotated

from app.dependencies.repository.repository import get_repository
from app.dependencies.user_roles.caller_user_dep import CallerUserDep
from app.repository.users_repository import UsersRepository
from app.services.users.users_service import UsersService


class Users:
    async def __call__(
        self,
        user: CallerUserDep,
        users_repository: UsersRepository = Depends(get_repository(UsersRepository)),
    ) -> UsersService:
        return UsersService(users_repository, user.id)  # TODO: change to only ID.


users_admin_service = Users()
UsersServiceDep = Annotated[UsersService, Depends(users_admin_service)]
