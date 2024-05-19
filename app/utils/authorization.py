from fastapi import HTTPException


def validate_caller(user_id: str, caller_id: str):
    if user_id != caller_id:
        raise HTTPException(
            status_code=403,
            detail="No permissions for this method"
        )
