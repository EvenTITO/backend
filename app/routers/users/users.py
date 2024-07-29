from app.dependencies.services.users.users_service_dep import UsersServiceDep
from app.schemas.users.user import UserSchema
from fastapi import APIRouter
from app.routers.users.roles import user_roles_router
from app.routers.users.echo import echo_router
from app.repository import users_crud
from app.utils.dependencies import CallerIdDep
from app.dependencies.database.session_dep import SessionDep
from app.services.users import users_service
from app.schemas.users.user import UserReply
from app.dependencies.user_roles.admin_user_dep import AdminDep
from app.dependencies.user_roles.same_user_or_admin_dep import SameUserOrAdminDep
from app.dependencies.user_roles.same_user_dep import SameUserDep


users_router = APIRouter(
    prefix="/users",
)

users_router.include_router(echo_router)
users_router.include_router(user_roles_router)


@users_router.get("/{user_id}", response_model=UserReply, tags=["Users: General"])
async def read_user(user_id: str, db: SessionDep, _: SameUserOrAdminDep):
    return await users_service.get_user_by_id(db, user_id)


@users_router.post("", status_code=201, response_model=str, tags=["Users: General"])
async def create_user(user: UserSchema, users_service: UsersServiceDep):
    user_created_id = await users_service.create(user)
    return user_created_id


@users_router.put("/{user_id}", status_code=204, response_model=None, tags=["Users: General"])
async def update_user(user: UserSchema, caller_user: SameUserDep, db: SessionDep):
    await users_service.update_user(db, caller_user, user)


@users_router.delete("/{user_id}", status_code=204, response_model=None, tags=["Users: General"])
async def delete_user(user_id: str, _: SameUserOrAdminDep, db: SessionDep):
    await users_service.delete_user(db, user_id)


@users_router.get("", response_model=list[UserReply], tags=["Users: Administration"])
async def read_all_users(_: AdminDep, db: SessionDep, skip: int = 0, limit: int = 100):
    return await users_crud.get_users(db, skip, limit)
