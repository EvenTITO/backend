from fastapi import Depends
from typing import Annotated

from app.dependencies.repository.repository import get_repository
from app.dependencies.user_roles.user_id_dep import UserIdDep
from app.repository.works import WorksRepository
from app.services.works.works_service import WorksService


class AuthUserWorksService:
    async def __call__(
        self,
        user_id: UserIdDep,
        event_id: str,
        works_repository: WorksRepository = Depends(get_repository(WorksRepository)),
    ) -> WorksService:
        return WorksService(works_repository=works_repository, user_id=user_id, event_id=event_id)


auth_works_service = AuthUserWorksService()
WorksServiceDep = Annotated[WorksService, Depends(auth_works_service)]
