from fastapi import HTTPException
from .crud_utils import get_user


def validate_user_permissions(db, caller_id, user_id=None):
    if (user_id == caller_id and user_id is not None):
        return

    db_caller = get_user(db, caller_id)
    if db_caller.is_superuser:
        return
    else:
        raise HTTPException(
            status_code=403,
            detail="Not permission for this method"
        )
