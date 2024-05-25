from typing import Annotated
from sqlalchemy.orm import Session
from app.users.model import UserModel, UserRole
from app.users.crud import get_user_by_id
from app.users.exceptions import UserNotFound
from fastapi import Header, HTTPException, Depends
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.database.database import SessionLocal


async def get_db() -> AsyncIterator[async_sessionmaker]:
    try:
        yield SessionLocal
    except Exception as e:
        print(e)


SessionDep = Annotated[Session, Depends(get_db)]


def get_user_id(X_User_Id: str = Header(...)) -> str:
    if not X_User_Id:
        raise HTTPException(status_code=400, detail="X-User-Id missing.")
    return X_User_Id


CallerIdDep = Annotated[str, Depends(get_user_id)]


def get_caller_user(caller_id: CallerIdDep, db: SessionDep) -> UserModel:
    user = get_user_by_id(db, caller_id)
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
