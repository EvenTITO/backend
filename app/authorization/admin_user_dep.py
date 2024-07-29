from app.services.users.users_service_dep import UsersServiceDep
from typing import Annotated
from app.database.models.user import UserRole
from fastapi import HTTPException, Depends


class AdminUser:
    async def __call__(self, service: UsersServiceDep) -> None:
        role = await service.get_role()
        if role != UserRole.ADMIN:
            raise HTTPException(status_code=403)


admin_user_checker = AdminUser()
AdminDep = Annotated[None, Depends(admin_user_checker)]
