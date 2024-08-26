from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.user_id_dep import UserDep
from app.repository.repository import get_repository
from app.repository.works_repository import WorksRepository
from app.services.works.works_service import WorksService


class Works:
    async def __call__(
            self,
            _: UserDep,
            caller_id: CallerIdDep,
            event_id: UUID,
            works_repository: WorksRepository = Depends(get_repository(WorksRepository)),
    ) -> WorksService:
        return WorksService(works_repository=works_repository, user_id=caller_id, event_id=event_id)


auth_works_service = Works()
WorksServiceDep = Annotated[WorksService, Depends(auth_works_service)]
