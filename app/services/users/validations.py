from app.repository import users_crud
from .exceptions import (
    UserNotFound,
)


async def validate_user_exists_with_id(db, id_user):
    user = await users_crud.get_user_by_id(db, id_user)
    if not user:
        raise UserNotFound(id_user)
