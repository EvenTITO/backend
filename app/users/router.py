from fastapi import APIRouter
from app.utils.dependencies import (
    SessionDep,
    CallerIdDep,
    AdminDep,
    SameUserOrAdminDep,
    SameUserDep,
)
from app.users import crud
from .schemas import UserRole
from .schemas import UserSchema, RoleSchema, UserReply
from typing import List
from .exceptions import (
    UserNotFound,
    IdAlreadyExists,
    EmailAlreadyExists,
    EmailCantChange,
    CantRemoveLastAdmin,
)


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@users_router.post("", status_code=201, response_model=str)
def create_user(user: UserSchema, db: SessionDep, caller_id: CallerIdDep):
    user_in_db = crud.get_user_by_id(db, caller_id)
    if user_in_db:
        raise IdAlreadyExists(caller_id)
    user_in_db = crud.get_user_by_email(db, user.email)
    if user_in_db:
        raise EmailAlreadyExists(user.email)

    user_created = crud.create_user(db=db, id=caller_id, user=user)
    return user_created.id


@users_router.patch(
    "/permissions/{user_id}", status_code=204, response_model=None
)
def update_user_permission(
    user_id: str, role: RoleSchema, caller_user: AdminDep, db: SessionDep
):
    # One can remove himself from Admin role, but there must be
    # always at least one admin.
    if (
        (caller_user.id == user_id)
        and (role.role != UserRole.ADMIN.value)
        and (crud.get_amount_admins(db) == 1)
    ):
        raise CantRemoveLastAdmin()

    crud.update_permission(db, user_id, role.role)


@users_router.get("/{user_id}", response_model=UserReply)
def read_user(user_id: str, db: SessionDep, _: SameUserOrAdminDep):
    user = crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise UserNotFound(user_id)
    return user


@users_router.get("", response_model=List[UserReply])
def read_all_users(
    _: AdminDep,
    db: SessionDep,
    skip: int = 0,
    limit: int = 100
):
    return crud.get_users(db, skip, limit)


@users_router.put("/{user_id}", status_code=204, response_model=None)
def update_user(
    user_id: str, user: UserSchema, caller_user: SameUserDep, db: SessionDep
):
    if user.email != caller_user.email:
        raise EmailCantChange(user.email, caller_user.email)

    crud.update_user(db=db, id=user_id, user_to_update=user)


@users_router.delete("/{user_id}", status_code=204, response_model=None)
def delete_user(user_id: str, _: SameUserOrAdminDep, db: SessionDep):
    user = crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise UserNotFound(user_id)

    crud.delete_user(db=db, user=user)
