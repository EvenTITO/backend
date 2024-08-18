from typing import Annotated

from fastapi import Depends

from app.authorization.caller_id_dep import CallerIdDep
from app.repository.repository import get_repository
from app.repository.submissions_repository import SubmissionsRepository
from app.repository.works_repository import WorksRepository
from app.services.storage.work_storage_service_dep import WorkStorageServiceDep
from app.services.submissions.submissions_service import SubmissionsService
from app.services.works.works_service import WorksService


class Submissions:
    async def __call__(
            self,
            user_id: CallerIdDep,
            event_id: str,
            work_id: str,
            storage_service: WorkStorageServiceDep,
            submission_repository: SubmissionsRepository = Depends(get_repository(SubmissionsRepository)),
            work_repository: WorksRepository = Depends(get_repository(WorksRepository))
    ) -> SubmissionsService:
        work_service = WorksService(work_repository, user_id, event_id)
        return SubmissionsService(
            submission_repository,
            work_service,
            storage_service,
            user_id,
            event_id,
            work_id
        )


submissions_service = Submissions()
SubmissionsServiceDep = Annotated[SubmissionsService, Depends(submissions_service)]
