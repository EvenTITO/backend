from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud import users
from app.schemas.users import UserSchema
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", response_model=UserSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    return users.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: str, db: Session = Depends(get_db)):
    return users.get_user(db, user_id=user_id)


@router.put("/", response_model=UserSchema)
def update_user(user: UserSchema, db: Session = Depends(get_db)):
    return users.update_user(db=db, user_updated=user)


@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    return users.delete_user(db=db, user_id=user_id)
