from typing import Annotated

from fastapi import HTTPException, Depends

from app.authorization.admin_user_dep import IsAdminUsrDep
from app.authorization.same_user_dep import IsSameUsrDep


class IsSameUserOrAdmin:
    async def __call__(self, is_same_user: IsSameUsrDep, is_admin: IsAdminUsrDep) -> bool:
        return is_same_user or is_admin


is_same_user_or_admin = IsSameUserOrAdmin()
IsSameUserOrAdmin = Annotated[bool, Depends(is_same_user_or_admin)]


class VerifyIsSameUserOrAdmin:
    async def __call__(self, is_my_user_or_admin: IsSameUserOrAdmin) -> None:
        if not is_my_user_or_admin:
            raise HTTPException(status_code=403)


verify_is_same_user_or_admin = VerifyIsSameUserOrAdmin()
VerifyIsSameUserOrAdminDep = Annotated[None, Depends(verify_is_same_user_or_admin)]
