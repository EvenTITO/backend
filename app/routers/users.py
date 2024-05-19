from sqlalchemy.orm import Session
from app.utils.dependencies import SessionDep, CallerIdDep
from app.crud import users
from app.schemas.users import UserSchema, UserSchemaWithId
from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[SessionDep, CallerIdDep]
)


@router.post("/", response_model=UserSchemaWithId)
def create_user(
    user: UserSchema,
    db: Session = SessionDep,
    user_id: str = CallerIdDep
):
    user_with_id = UserSchemaWithId(
        **user.model_dump(),
        id=user_id
    )
    return users.create_user(db=db, user=user_with_id)


@router.get("/{user_id}", response_model=UserSchemaWithId)
def read_user(
    user_id: str,
    db: Session = SessionDep
):
    return users.get_user(db, user_id=user_id)


@router.put("/", response_model=UserSchemaWithId)
def update_user(
    user: UserSchema,
    db: Session = SessionDep,
    user_id: str = CallerIdDep
):
    user_with_id = UserSchemaWithId(
        **user.model_dump(),
        id=user_id
    )
    return users.update_user(db=db, user_updated=user_with_id)


@router.delete("/{user_id}", response_model=UserSchemaWithId)
def delete_user(
    user_id: str,
    db: Session = SessionDep
):
    return users.delete_user(db=db, user_id=user_id)
