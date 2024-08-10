from app.database.models.work import WorkStates
from app.repository.submissions_repository import SubmissionsRepository
from app.schemas.works.submission import SubmissionSchema
from app.services.services import BaseService
from app.services.storage.work_storage_service import WorkStorageService
from app.services.works.author_works_service import AuthorWorksService


class AuthorSubmissionsService(BaseService):
    def __init__(self,
                 submission_repository: SubmissionsRepository,
                 work_service: AuthorWorksService,
                 storage_service: WorkStorageService,
                 user_id: str,
                 event_id: str,
                 work_id: int):
        self.submission_repository = submission_repository
        self.work_service = work_service
        self.storage_service = storage_service
        self.user_id = user_id
        self.event_id = event_id
        self.work_id = work_id

    async def do_submit(self) -> SubmissionSchema:
        await self.work_service.validate_update_work()
        my_work = await self.work_service.get_work()
        if my_work.state == WorkStates.RE_SUBMIT:
            submission = await self.submission_repository.do_new_submit(self.event_id, self.work_id)
        else:
            submission = await self.submission_repository.update_submit(self.event_id, self.work_id)
        upload_url = await self.storage_service.get_submission_upload_url(self.event_id, self.work_id, submission.id)
        return SubmissionSchema(id=submission.id, upload_url=upload_url)
