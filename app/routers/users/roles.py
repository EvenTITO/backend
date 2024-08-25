from fastapi import APIRouter, Depends

from app.authorization.admin_user_dep import verify_is_admin_user
from app.schemas.users.user_role import UserRoleSchema
from app.services.users.users_admin_service_dep import UsersAdminServiceDep

user_roles_router = APIRouter(
    prefix="/{user_id}/roles",
    tags=["Users: Roles"],
)


@user_roles_router.patch("", status_code=204, response_model=None, dependencies=[Depends(verify_is_admin_user)])
async def update_user_role(user_id: str, role: UserRoleSchema, users_admin_service: UsersAdminServiceDep):
    await users_admin_service.update_role(user_id, role)
