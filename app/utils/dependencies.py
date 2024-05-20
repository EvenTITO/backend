from typing import Annotated
from sqlalchemy.orm import Session
from app.users.model import UserModel
from app.users.crud import USER_NOT_FOUND_DETAIL
from app.utils.crud_utils import get_user
from fastapi import Header, HTTPException, Depends
from app.database.database import SessionLocal
from sqlalchemy.exc import NoResultFound


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
    try:
        user = get_user(db, caller_id)
        return user
    except NoResultFound:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND_DETAIL)


CallerUserDep = Annotated[UserModel, Depends(get_caller_user)]
