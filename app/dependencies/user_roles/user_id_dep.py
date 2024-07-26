from fastapi import Depends
from typing import Annotated

from app.database.dependencies import SessionDep
from app.repository.users_crud import get_user_by_id
from app.services.users.exceptions import UserNotFound
from app.utils.dependencies import CallerIdDep


class UserId:
    async def __call__(
        self,
        caller_id: CallerIdDep,
        db: SessionDep
    ) -> str:
        user = await get_user_by_id(db, caller_id)
        if not user:
            raise UserNotFound(caller_id)
        return user.id
# TODO: esta devolviendo el id, deberia cambiar a que el crud soporte la llamada de si existe.


user_id_exists_checker = UserId()
UserIdDep = Annotated[str, Depends(user_id_exists_checker)]
