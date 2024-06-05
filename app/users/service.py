from app.users import crud, validations


async def get_user(db, user_id):
    user = await crud.get_user_by_id(db, user_id=user_id)
    validations.validate_user_exists(user, user_id)
    return user


async def get_user_by_email(db, email):
    user = await crud.get_user_by_email(db, email)
    validations.validate_user_exists(user, email)
    return user
