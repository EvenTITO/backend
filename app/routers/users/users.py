from fastapi import APIRouter, Depends
from app.authorization.caller_id_dep import verify_user_id
from app.authorization.user_id_dep import verify_user_exists
from app.services.users.users_admin_service_dep import UsersAdminServiceDep
from app.services.users.users_service_dep import UsersServiceDep
from app.schemas.users.user import UserModifySchema, UserSchema
from app.routers.users.roles import user_roles_router
from app.routers.users.echo import echo_router
from app.schemas.users.user import UserReply
from app.authorization.same_user_or_admin_dep import verify_same_user_or_admin
from app.authorization.admin_user_dep import verify_user_is_admin

users_router = APIRouter(
    prefix="/users",
)

users_router.include_router(echo_router)
users_router.include_router(user_roles_router)


@users_router.get(
    "/{user_id}",
    response_model=UserReply,
    tags=["Users: General"],
    dependencies=[Depends(verify_same_user_or_admin)]
)
async def read_user(user_id: str, users_service: UsersServiceDep):
    return await users_service.get(user_id)


@users_router.post(
    "",
    status_code=201,
    response_model=str,
    tags=["Users: General"],
    dependencies=[Depends(verify_user_id)]
)
async def create_user(user: UserSchema, users_service: UsersServiceDep):
    user_created_id = await users_service.create(user)
    return user_created_id


@users_router.put(
    "/{user_id}",
    status_code=204,
    response_model=None,
    tags=["Users: General"],
    dependencies=[Depends(verify_user_exists)]
)
async def update_user(user: UserModifySchema, users_service: UsersServiceDep):
    await users_service.update(user)


@users_router.get(
    "",
    response_model=list[UserReply],
    tags=["Users: Administration"],
    dependencies=[Depends(verify_user_is_admin)]
)
async def read_all_users(users_admin_service: UsersAdminServiceDep, limit: int = 100, offset: int = 0):
    return await users_admin_service.get_many(limit, offset)
