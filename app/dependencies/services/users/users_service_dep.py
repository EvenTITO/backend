from fastapi import Depends
from typing import Annotated

from app.dependencies.repository.repository import get_repository
from app.repository.users import UsersRepository
from app.services.users.users_service import UsersService
from app.utils.dependencies import CallerIdDep


class Users:
    async def __call__(
        self,
        user_id: CallerIdDep,
        users_repository: UsersRepository = Depends(get_repository(UsersRepository)),
    ) -> UsersService:
        return UsersService(users_repository, user_id)


users_admin_service = Users()
UsersServiceDep = Annotated[UsersService, Depends(users_admin_service)]
