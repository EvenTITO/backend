from typing import Annotated
# from app.users.model import UserModel, UserRole
# from app.users.crud import get_user_by_id
# from app.users.exceptions import UserNotFound
from fastapi import Header, HTTPException, Depends
# from app.database.dependencies import SessionDep


async def get_user_id(X_User_Id: str = Header(...)) -> str:
    if not X_User_Id:
        raise HTTPException(status_code=400, detail="X-User-Id missing.")
    return X_User_Id


CallerIdDep = Annotated[str, Depends(get_user_id)]


# def get_creator_user(caller_user: CallerUserDep) -> UserModel:
#     if (
#         (caller_user.role == UserRole.ADMIN) or
#         (caller_user.role == UserRole.EVENT_CREATOR)
#     ):
#         return caller_user
#     else:
#         raise HTTPException(status_code=403)


# CreatorDep = Annotated[UserModel, Depends(get_creator_user)]
