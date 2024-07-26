from fastapi import APIRouter

from app.database.dependencies import SessionDep
from app.dependencies.user_roles.admin_user_dep import AdminDep
from app.services.users import users_service
from app.schemas.users.user_role import UserRoleSchema


user_roles_router = APIRouter(
    prefix="/{user_id}/roles",
    tags=["Users: Roles"],
)


@user_roles_router.patch("", status_code=204, response_model=None)
async def update_user_role(user_id: str, role: UserRoleSchema, admin_user: AdminDep, db: SessionDep):
    await users_service.update_role(db, admin_user.id, user_id, role.role)
