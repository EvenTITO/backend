from app.schemas.users.user import UserSchema
from fastapi import APIRouter
from app.routers.users.roles import user_roles_router
from app.routers.users.echo import echo_router
from app.repository import users_crud
from app.utils.dependencies import CallerIdDep
from app.database.dependencies import SessionDep
from app.users.dependencies import (
    SameUserOrAdminDep,
    SameUserDep,
)
from app.users import validations
from app.users.service import get_user
from app.schemas.users.user import UserReply
from app.users.dependencies import AdminDep


users_router = APIRouter(
    prefix="/users",
)

users_router.include_router(echo_router)
users_router.include_router(user_roles_router)


@users_router.get(
    "/{user_id}",
    response_model=UserReply,
    tags=["Users: General"]
)
async def read_user(user_id: str, db: SessionDep, _: SameUserOrAdminDep):
    return await get_user(db, user_id)


@users_router.post(
    "",
    status_code=201,
    response_model=str,
    tags=["Users: General"]
)
async def create_user(user: UserSchema,
                      db: SessionDep, caller_id: CallerIdDep):
    await validations.validate_user_not_exists(db, caller_id, user.email)
    user_created = await users_crud.create_user(db=db, id=caller_id, user=user)
    return user_created.id


@users_router.put(
    "/{user_id}",
    status_code=204,
    response_model=None,
    tags=["Users: General"]
)
async def update_user(
    user: UserSchema, caller_user: SameUserDep, db: SessionDep
):
    validations.validate_user_change(user, caller_user)
    await users_crud.update_user(
        db=db,
        current_user=caller_user,
        user_to_update=user
    )


@users_router.delete(
    "/{user_id}",
    status_code=204,
    response_model=None,
    tags=["Users: General"]
)
async def delete_user(user_id: str, _: SameUserOrAdminDep, db: SessionDep):
    user = await get_user(db, user_id)
    await users_crud.delete_user(db=db, user=user)


@users_router.get(
    "",
    response_model=list[UserReply],
    tags=["Users: Administration"]
)
async def read_all_users(
    _: AdminDep,
    db: SessionDep,
    skip: int = 0,
    limit: int = 100
):
    return await users_crud.get_users(db, skip, limit)
