from app.repository import users_crud
from app.services.users.exceptions import UserNotFound


async def get_user_by_id(db, user_id):
    user = await users_crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise UserNotFound(user_id)
    return user


async def get_user_by_email(db, email):
    user = await users_crud.get_user_by_email(db, email)
    if not user:
        raise UserNotFound(email)
    return user
