from fastapi import Depends
from typing import Annotated

from app.dependencies.repository.repository import get_repository
from app.utils.dependencies import CallerIdDep
from app.repository.works_repository import WorksRepository
from app.services.works.author_works_service import AuthorWorksService


class AuthorWorks:
    async def __call__(
        self,
        user_id: CallerIdDep,
        event_id: str,
        work_id: int,
        works_repository: WorksRepository = Depends(get_repository(WorksRepository)),
    ) -> AuthorWorksService:
        return AuthorWorksService(works_repository, user_id, event_id, work_id)


author_works_service = AuthorWorks()
AuthorWorksServiceDep = Annotated[AuthorWorksService, Depends(author_works_service)]
