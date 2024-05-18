from sqlalchemy.orm import Session
from app.utils.dependencies import get_db, get_user_id
from app.crud import users
from app.schemas.users import UserSchema, UserSchemaWithId
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_user_id), Depends(get_db)]
)


@router.post("/", response_model=UserSchema)
def create_user(
    user: UserSchema,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    user_with_id = UserSchemaWithId(
        **user.dict(),
        id=user_id
    )
    return users.create_user(db=db, user=user_with_id)


@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    return users.get_user(db, user_id=user_id)


@router.put("/", response_model=UserSchema)
def update_user(
    user: UserSchema,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    user_with_id = UserSchemaWithId(
        **user.dict(),
        id=user_id
    )
    return users.update_user(db=db, user_updated=user_with_id)


@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    return users.delete_user(db=db, user_id=user_id)
