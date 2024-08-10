from typing import Annotated

from fastapi import Depends

from app.authorization.caller_id_dep import CallerIdDep
from app.repository.repository import get_repository
from app.repository.submissions_repository import SubmissionsRepository
from app.repository.works_repository import WorksRepository
from app.services.storage.work_storage_service import WorkStorageService
from app.services.storage.work_storage_service_dep import WorkStorageServiceDep
from app.services.submissions.author_submissions_service import AuthorSubmissionsService
from app.services.works.author_works_service import AuthorWorksService


class AuthorSubmissions:
    async def __call__(
            self,
            user_id: CallerIdDep,
            event_id: str,
            work_id: int,
            storage_service: WorkStorageService = WorkStorageServiceDep,
            submission_repository: SubmissionsRepository = Depends(get_repository(SubmissionsRepository)),
            work_repository: WorksRepository = Depends(get_repository(WorksRepository))
    ) -> AuthorSubmissionsService:
        work_service = AuthorWorksService(work_repository, user_id, event_id, work_id)
        return AuthorSubmissionsService(
            submission_repository,
            work_service,
            storage_service,
            user_id,
            event_id,
            work_id
        )


author_submissions_service = AuthorSubmissions()
AuthorSubmissionsServiceDep = Annotated[AuthorSubmissionsService, Depends(author_submissions_service)]
