from fastapi import Depends
from typing import Annotated

from app.repository.repository import get_repository
from app.authorization.admin_user_dep import AdminDep
from app.repository.users_repository import UsersRepository
from app.services.users.users_admin_service import UsersAdminService
from app.utils.dependencies import CallerIdDep


class UsersAdmin:
    async def __call__(
        self,
        user_id: CallerIdDep,
        _: AdminDep,
        users_repository: UsersRepository = Depends(get_repository(UsersRepository)),
    ) -> UsersAdminService:
        return UsersAdminService(users_repository, user_id)


users_admin_service = UsersAdmin()
UsersAdminServiceDep = Annotated[UsersAdminService, Depends(users_admin_service)]
