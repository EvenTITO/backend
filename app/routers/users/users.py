from fastapi import APIRouter
from app.dependencies.services.users.pubilc_users_service_dep import PublicUsersServiceDep
from app.dependencies.services.users.users_admin_service_dep import UsersAdminServiceDep
from app.dependencies.services.users.users_service_dep import UsersServiceDep
from app.schemas.users.user import UserModifySchema, UserSchema
from app.routers.users.roles import user_roles_router
from app.routers.users.echo import echo_router
from app.database.session_dep import SessionDep
from app.services.users import users_service
from app.schemas.users.user import UserReply
from app.authorization.same_user_or_admin_dep import SameUserOrAdminDep


users_router = APIRouter(
    prefix="/users",
)

users_router.include_router(echo_router)
users_router.include_router(user_roles_router)


@users_router.get("/{user_id}", response_model=UserReply, tags=["Users: General"])
async def read_user(user_id: str, db: SessionDep, _: SameUserOrAdminDep):
    return await users_service.get_user_by_id(db, user_id)


@users_router.post("", status_code=201, response_model=str, tags=["Users: General"])
async def create_user(user: UserSchema, users_service: PublicUsersServiceDep):
    user_created_id = await users_service.create(user)
    return user_created_id


@users_router.put("/me", status_code=204, response_model=None, tags=["Users: General"])
async def update_user(user: UserModifySchema, users_service: UsersServiceDep):
    await users_service.update(user)


@users_router.get("", response_model=list[UserReply], tags=["Users: Administration"])
async def read_all_users(users_admin_service: UsersAdminServiceDep, limit: int = 100, offset: int = 0):
    return await users_admin_service.get_many(limit, offset)
