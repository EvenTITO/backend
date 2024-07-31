from app.repository import users_crud
from ...exceptions.users_exceptions import (
    UserNotFound,
)


async def validate_user_exists_with_id(db, user_id):
    user = await users_crud.get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound(user_id)
