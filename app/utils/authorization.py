from fastapi import HTTPException
from .crud_utils import get_user
from app.users.model import UserModel
from app.events.crud import is_creator
from app.organizers.crud import is_organizer, EVENT_ORGANIZER_NOT_FOUND

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


def validate_user_creator_or_organizer(db, event_id, user_id):
    if (not is_organizer(db, event_id, user_id) and not is_creator(db, event_id, user_id)):
        raise HTTPException(
            status_code=404,
            detail=EVENT_ORGANIZER_NOT_FOUND
        )
