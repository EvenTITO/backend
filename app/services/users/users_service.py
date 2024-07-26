from app.models.user import UserRole
from app.repository import users_crud
from app.services.users.exceptions import (
    CantRemoveLastAdmin,
    EmailAlreadyExists,
    EmailCantChange,
    IdAlreadyExists,
    UserNotFound
)


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


async def get_users(db, skip, limit):
    return await users_crud.get_users(db, skip, limit)


async def create_user(db, user_id, user):
    user_in_db = await users_crud.get_user_by_id(db, user_id)
    if user_in_db:
        raise IdAlreadyExists(user_id)
    user_in_db = await users_crud.get_user_by_email(db, user.email)
    if user_in_db:
        raise EmailAlreadyExists(user.email)

    user_created = await users_crud.create_user(db=db, id=user_id, user=user)
    return user_created.id


async def update_user(db, current_user, user_with_update):
    if current_user.email != user_with_update.email:
        raise EmailCantChange(current_user.email, user_with_update.email)
    await users_crud.update_user(db, current_user, user_with_update)


async def update_role(db, admin_user_id, user_id, user_role_update):
    await __validate_always_at_least_one_admin(db, user_id, admin_user_id, user_role_update)

    current_user = await get_user_by_id(db, user_id)
    await users_crud.update_role(db, current_user, user_role_update)


async def delete_user(db, user_id):
    user = await get_user_by_id(db, user_id)
    await users_crud.delete_user(db, user)


async def __validate_always_at_least_one_admin(db, user_id, admin_user_id, role):
    """
    One can remove himself from Admin role, but there must be
    always at least one admin.
    """
    if (
            (admin_user_id == user_id)
            and (role != UserRole.ADMIN)
            and (await users_crud.get_amount_admins(db) == 1)
    ):
        raise CantRemoveLastAdmin()
