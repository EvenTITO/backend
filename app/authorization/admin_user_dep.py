from typing import Annotated

from fastapi import HTTPException, Depends

from app.authorization.user_id_dep import UserDep
from app.database.models.user import UserRole


class IsAdminUser:
    async def __call__(self, role: UserDep) -> bool:
        return role == UserRole.ADMIN


is_admin_user = IsAdminUser()
IsAdminUsrDep = Annotated[bool, Depends(is_admin_user)]


class VerifyIsAdminUser:
    async def __call__(self, is_admin: IsAdminUsrDep) -> None:
        if not is_admin:
            raise HTTPException(status_code=403)


verify_user_is_admin = VerifyIsAdminUser()
AdminUsrDep = Annotated[None, Depends(verify_user_is_admin)]
