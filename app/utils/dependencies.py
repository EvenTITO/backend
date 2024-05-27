from typing import Annotated
from app.users.model import UserModel, UserRole
from app.users.crud import get_user_by_id
from app.users.exceptions import UserNotFound
from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import SessionLocal


async def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_db)]
# SessionDep = Depends(get_db)


async def get_user_id(X_User_Id: str = Header(...)) -> str:
    if not X_User_Id:
        raise HTTPException(status_code=400, detail="X-User-Id missing.")
    return X_User_Id


CallerIdDep = Annotated[str, Depends(get_user_id)]


async def get_caller_user(caller_id: CallerIdDep, db: SessionDep) -> UserModel:
    user = await get_user_by_id(db, caller_id)
    if not user:
        raise UserNotFound(caller_id)

    return user


CallerUserDep = Annotated[UserModel, Depends(get_caller_user)]


def get_admin_user(caller_user: CallerUserDep) -> UserModel:
    if caller_user.role == UserRole.ADMIN:
        return caller_user
    else:
        raise HTTPException(status_code=403)


AdminDep = Annotated[UserModel, Depends(get_admin_user)]


def get_creator_user(caller_user: CallerUserDep) -> UserModel:
    if (
        (caller_user.role == UserRole.ADMIN) or
        (caller_user.role == UserRole.EVENT_CREATOR)
    ):
        return caller_user
    else:
        raise HTTPException(status_code=403)


CreatorDep = Annotated[UserModel, Depends(get_creator_user)]
