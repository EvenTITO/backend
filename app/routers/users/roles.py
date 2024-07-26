from fastapi import APIRouter

from app.repository import users_crud
from app.database.dependencies import SessionDep
from app.dependencies.admin_user_dep import AdminDep
from app.users import validations
from app.users.service import get_user
from app.schemas.users.user_role import UserRoleSchema


user_roles_router = APIRouter(
    prefix="/{user_id}/roles",
    tags=["Users: Roles"],
)


@user_roles_router.patch("", status_code=204, response_model=None)
async def update_user_role(
    user_id: str, role: UserRoleSchema, caller_user: AdminDep, db: SessionDep
):
    await validations.validate_always_at_least_one_admin(
        db,
        user_id,
        caller_user,
        role
    )
    current_user = await get_user(db, user_id)
    await users_crud.update_role(db, current_user, role.role)
