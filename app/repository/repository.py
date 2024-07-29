from app.database.session_dep import SessionDep
from typing import Type

from app.utils.crud_repository import CRUDBRepository


def get_repository(repository: Type[CRUDBRepository]):
    async def _get_repository(session: SessionDep):
        return repository(session)

    return _get_repository
