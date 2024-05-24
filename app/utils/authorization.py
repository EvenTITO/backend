from fastapi import HTTPException
from app.events.crud import is_creator
from app.users import crud
from app.organizers.crud import is_organizer, EVENT_ORGANIZER_NOT_FOUND

NOT_PERMISSION_ERROR = "Not permission for this method"


def validate_same_user_or_superuser(db, user_id, caller_id: str):
    if (user_id == caller_id):
        return
    validate_superuser(db, caller_id)


def validate_user_permissions(user_id, caller_id: str):
    if (user_id == caller_id):
        return
    else:
        raise HTTPException(
            status_code=403,
            detail=NOT_PERMISSION_ERROR
        )


def validate_superuser(db, caller_id):
    db_caller = crud.get_user_by_id(db, caller_id)
    if db_caller and db_caller.is_superuser:
        return
    else:
        raise HTTPException(
            status_code=403,
            detail=NOT_PERMISSION_ERROR
        )


def validate_user_creator_or_organizer(db, event_id, user_id):
    if (not is_organizer(db, event_id, user_id) and
            not is_creator(db, event_id, user_id)):
        raise HTTPException(
            status_code=404,
            detail=EVENT_ORGANIZER_NOT_FOUND
        )
