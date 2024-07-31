from app.authorization.user_id_dep import UserDep
from typing import Annotated
from app.database.models.user import UserRole
from fastapi import HTTPException, Depends


class AdminUser:
    async def __call__(self, role: UserDep) -> None:
        if role != UserRole.ADMIN:
            raise HTTPException(status_code=403)


verify_user_is_admin = AdminUser()
AdminDep = Annotated[None, Depends(verify_user_is_admin)]
