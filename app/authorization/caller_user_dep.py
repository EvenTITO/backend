from fastapi import Depends
from typing import Annotated

from app.database.session_dep import SessionDep
from app.database.models.user import UserModel
from app.repository.users_crud import get_user_by_id
from app.services.users.exceptions import UserNotFound
from app.utils.dependencies import CallerIdDep


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


caller_user_checker = CallerUser()
CallerUserDep = Annotated[UserModel, Depends(caller_user_checker)]
