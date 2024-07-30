from fastapi import Depends
from typing import Annotated

from app.database.session_dep import SessionDep
from app.database.models.user import UserModel
from app.repository.users_crud import get_user_by_id
from app.services.users.exceptions import UserNotFound
from app.authorization.caller_id_dep import CallerIdDep

# TODO: remove this class and use UserIdDep. This class is deprecated.
class CallerUser:
    async def __call__(
        self,
        caller_id: CallerIdDep,
        db: SessionDep
    ) -> UserModel:
        user = await get_user_by_id(db, caller_id)
        if not user:
            raise UserNotFound(caller_id)
        return user


verify_user_exists = CallerUser()
CallerUserDep = Annotated[UserModel, Depends(verify_user_exists)]
