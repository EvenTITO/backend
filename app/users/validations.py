from app.users import crud
from .exceptions import (
    IdAlreadyExists,
    EmailAlreadyExists,
    CantRemoveLastAdmin,
    UserNotFound,
    EmailCantChange
)
from .model import UserRole


async def validate_user_exists_with_id(db, id_user):
    user = await crud.get_user_by_id(db, id_user)
    if not user:
        raise UserNotFound(id_user)


async def validate_user_not_exists(db, id_user, email):
    user_in_db = await crud.get_user_by_id(db, id_user)
    if user_in_db:
        raise IdAlreadyExists(id_user)
    user_in_db = await crud.get_user_by_email(db, email)
    if user_in_db:
        raise EmailAlreadyExists(email)


async def validate_always_at_least_one_admin(db, user_id, caller_user, role):
    # One can remove himself from Admin role, but there must be
    # always at least one admin.
    if (
            (caller_user.id == user_id)
            and (role.role != UserRole.ADMIN)
            and (await crud.get_amount_admins(db) == 1)
    ):
        raise CantRemoveLastAdmin()


def validate_user_exists(user, user_id):
    if not user:
        raise UserNotFound(user_id)


def validate_user_change(user, caller_user):
    if user.email != caller_user.email:
        raise EmailCantChange(user.email, caller_user.email)
