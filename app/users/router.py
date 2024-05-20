from app.utils.authorization import validate_user_permissions
from app.utils.dependencies import (
    SessionDep,
    CallerIdDep,
    CallerUserDep,
    AdminDep
)
from app.users import crud
from .schemas import (
    UserSchema,
    UserSchemaWithId,
    RoleSchema,
    CompleteUser
)
from fastapi import APIRouter


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@users_router.post("/", response_model=UserSchemaWithId)
def create_user(
    user: UserSchema,
    db: SessionDep,
    caller_id: CallerIdDep,
):
    user_with_id = UserSchemaWithId(
        **user.model_dump(),
        id=caller_id
    )
    return crud.create_user(db=db, user=user_with_id)


@users_router.patch("/permissions/{user_id}", response_model=CompleteUser)
def update_user_permission(
    user_id: str,
    role: RoleSchema,
    _: AdminDep,
    db: SessionDep
):
    return crud.update_permission(db, user_id, role.role)


@users_router.get("/{user_id}", response_model=CompleteUser)
def read_user(
    user_id: str,
    db: SessionDep
):
    return crud.get_user_by_id(
        db,
        user_id=user_id
    )


@users_router.put("/", response_model=UserSchemaWithId)
def update_user(
    user: UserSchema,
    caller_id: CallerIdDep,
    db: SessionDep
):
    user_with_id = UserSchemaWithId(
        **user.model_dump(),
        id=caller_id
    )
    return crud.update_user(db=db, user_updated=user_with_id)


@users_router.delete("/{user_id}", response_model=UserSchemaWithId)
def delete_user(
    user_id: str,
    caller_user: CallerUserDep,
    db: SessionDep
):
    validate_user_permissions(user_id, caller_user)
    return crud.delete_user(db=db, user_id=user_id)
