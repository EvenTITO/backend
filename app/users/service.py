from app.repository import users_crud
from app.users import validations


async def get_user(db, user_id):
    user = await users_crud.get_user_by_id(db, user_id=user_id)
    validations.validate_user_exists(user, user_id)
    return user


async def get_user_by_email(db, email):
    user = await users_crud.get_user_by_email(db, email)
    validations.validate_user_exists(user, email)
    return user
