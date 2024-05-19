from sqlalchemy.orm import Session
from app.utils.dependencies import SessionDep, CallerIdDep
from app.users import crud
from .schemas import UserSchema, UserSchemaWithId
from fastapi import APIRouter


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[SessionDep, CallerIdDep]
)


@users_router.post("/", response_model=UserSchemaWithId)
def create_user(
    user: UserSchema,
    db: Session = SessionDep,
    caller_id: str = CallerIdDep
):
    user_with_id = UserSchemaWithId(
        **user.model_dump(),
        id=caller_id
    )
    return crud.create_user(db=db, user=user_with_id)


@users_router.get("/{user_id}", response_model=UserSchemaWithId)
def read_user(
    user_id: str,
    caller_id: str = CallerIdDep,
    db: Session = SessionDep
):
    return crud.get_user_by_id(
        db,
        user_id=user_id,
        caller_id=caller_id
    )


@users_router.put("/", response_model=UserSchemaWithId)
def update_user(
    user: UserSchema,
    caller_id: str = CallerIdDep,
    db: Session = SessionDep
):
    user_with_id = UserSchemaWithId(
        **user.model_dump(),
        id=caller_id
    )
    return crud.update_user(db=db, user_updated=user_with_id)


@users_router.delete("/{user_id}", response_model=UserSchemaWithId)
def delete_user(
    user_id: str,
    caller_id: str = CallerIdDep,
    db: Session = SessionDep
):
    return crud.delete_user(db=db, user_id=user_id, caller_id=caller_id)
