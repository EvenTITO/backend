from typing import Annotated

from fastapi import HTTPException, Depends

from app.authorization.caller_id_dep import CallerIdDep


class IsSameUser:
    async def __call__(self, user_id: str, caller_id: CallerIdDep) -> bool:
        return user_id == caller_id


IsSameUsrDep = Annotated[bool, Depends(IsSameUser())]


class VerifyIsSameUser:
    async def __call__(self, is_my_user: IsSameUsrDep) -> None:
        if not is_my_user:
            raise HTTPException(status_code=403)


verify_is_same_user = VerifyIsSameUser()
VerifyIsSameUsrDep = Annotated[None, Depends(verify_is_same_user)]
