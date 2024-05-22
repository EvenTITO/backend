from app.utils.authorization import (
    validate_user_permissions,
    validate_same_user_or_superuser
)
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
from typing import List

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@users_router.post("", status_code=201)
def create_user(
    user: UserSchema,
    db: SessionDep,
    caller_id: CallerIdDep,
) -> str:
    user_with_id = UserSchemaWithId(
        **user.model_dump(),
        id=caller_id
    )
    user_created = crud.create_user(db=db, user=user_with_id)
    return user_created.id


@users_router.patch("/permissions/{user_id}", status_code=204)
def update_user_permission(
    user_id: str,
    role: RoleSchema,
    _: AdminDep,
    db: SessionDep
):
    crud.update_permission(db, user_id, role.role)


@users_router.get("/{user_id}", response_model=CompleteUser)
def read_user(
    user_id: str,
    db: SessionDep
):
    return crud.get_user_by_id(
        db,
        user_id=user_id
    )


@users_router.get("", response_model=List[CompleteUser])
def read_all_users(
    _: AdminDep,
    db: SessionDep,
    skip: int = 0,
    limit: int = 100,
):
    return crud.get_users(db, skip, limit)


@users_router.put("/{user_id}", status_code=204)
def update_user(
    user_id: str,
    user: UserSchema,
    caller_id: CallerIdDep,
    db: SessionDep
):
    validate_user_permissions(user_id, caller_id)
    user_with_id = UserSchemaWithId(
        **user.model_dump(),
        id=user_id
    )
    crud.update_user(db=db, user_updated=user_with_id)


@users_router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: str,
    caller_user: CallerUserDep,
    db: SessionDep
):
    validate_same_user_or_superuser(db, user_id, caller_user.id)
    crud.delete_user(db=db, user_id=user_id)
