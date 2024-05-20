from fastapi import HTTPException
from .crud_utils import get_user
from app.users.model import UserModel

NOT_PERMISSION_ERROR = "Not permission for this method"


def validate_user_permissions(user_id, caller_user: UserModel):
    if (user_id == caller_user.id):
        return
    else:
        raise HTTPException(
            status_code=403,
            detail=NOT_PERMISSION_ERROR
        )


def validate_superuser(db, caller_id):
    db_caller = get_user(db, caller_id)
    if db_caller.is_superuser:
        return
    else:
        raise HTTPException(
            status_code=403,
            detail=NOT_PERMISSION_ERROR
        )
