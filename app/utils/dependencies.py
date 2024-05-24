from typing import Annotated
from sqlalchemy.orm import Session
from app.users.model import UserModel, UserRole
from app.users.crud import get_user_by_id
from app.users.exceptions import UserNotFound
from fastapi import Header, HTTPException, Depends
from app.database.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


class SameUserOrAdmin:
    def __call__(self, user_id: str, caller_user: CallerUserDep):
        if user_id != caller_user.id and caller_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403)

        return caller_user


same_user_or_admin = SameUserOrAdmin()
SameUserOrAdminDep = Annotated[UserModel, Depends(same_user_or_admin)]


class SameUser:
    def __call__(self, user_id: str, caller_user: CallerUserDep):
        if user_id != caller_user.id:
            raise HTTPException(status_code=403)
        return caller_user


same_user = SameUser()
SameUserDep = Annotated[UserModel, Depends(same_user)]
