from typing import Annotated
from fastapi import HTTPException, Header, Depends
from pydantic import BaseModel, ValidationError

from app.schemas.users.utils import UID


class UIDModel(BaseModel):
    uid: UID


async def verify_user_id(X_User_Id: Annotated[UID, Header()]) -> UID:
    return X_User_Id
    try:
        return UIDModel(uid=X_User_Id).uid  # force validation
    except ValidationError:
        raise HTTPException(status_code=400, detail="X-User-Id missing.")


CallerIdDep = Annotated[UID, Depends(verify_user_id)]
