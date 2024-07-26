from fastapi import APIRouter
from app.repository import users_crud
from app.utils.dependencies import CallerIdDep
from app.database.dependencies import SessionDep
from app.users.dependencies import AdminDep
from app.routers.users.roles import user_roles_router
from app.routers.users.echo import echo_router
from ...users.dependencies import (
    SameUserOrAdminDep,
    SameUserDep,
)
from app.users import validations
from app.users.service import get_user
from ...users.schemas import UserSchema, UserReply
from typing import List


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

users_router.include_router(user_roles_router)
users_router.include_router(echo_router)


@users_router.post("", status_code=201, response_model=str)
async def create_user(user: UserSchema,
                      db: SessionDep, caller_id: CallerIdDep):
    await validations.validate_user_not_exists(db, caller_id, user.email)
    user_created = await users_crud.create_user(db=db, id=caller_id, user=user)
    return user_created.id


@users_router.get("/{user_id}", response_model=UserReply)
async def read_user(user_id: str, db: SessionDep, _: SameUserOrAdminDep):
    return await get_user(db, user_id)


@users_router.get("", response_model=List[UserReply])
async def read_all_users(
    _: AdminDep,
    db: SessionDep,
    skip: int = 0,
    limit: int = 100
):
    return await users_crud.get_users(db, skip, limit)


@users_router.put("/{user_id}", status_code=204, response_model=None)
async def update_user(
    user: UserSchema, caller_user: SameUserDep, db: SessionDep
):
    validations.validate_user_change(user, caller_user)
    await users_crud.update_user(
        db=db,
        current_user=caller_user,
        user_to_update=user
    )


@users_router.delete("/{user_id}", status_code=204, response_model=None)
async def delete_user(user_id: str, _: SameUserOrAdminDep, db: SessionDep):
    user = await get_user(db, user_id)
    await users_crud.delete_user(db=db, user=user)
