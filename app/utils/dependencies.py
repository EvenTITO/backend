from typing import Annotated
from fastapi import Header, HTTPException, Depends
from app.database.database import SessionLocal


def get_user_id(X_User_Id: str = Header(...)):
    if not X_User_Id:
        raise HTTPException(status_code=400, detail="X-User-Id missing.")
    return X_User_Id


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Depends(get_db)
CallerIdDep = Depends(get_user_id)
