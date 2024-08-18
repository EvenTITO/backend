from app.database.models.submission import SubmissionModel
from app.database.models.work import WorkStates
from app.repository.submissions_repository import SubmissionsRepository
from app.schemas.works.submission import SubmissionUploadSchema, SubmissionDownloadSchema, SubmissionResponseSchema
from app.services.services import BaseService
from app.services.storage.work_storage_service import WorkStorageService
from app.services.works.works_service import WorksService


class SubmissionsService(BaseService):
    def __init__(self,
                 submission_repository: SubmissionsRepository,
                 work_service: WorksService,
                 storage_service: WorkStorageService,
                 user_id: str,
                 event_id: str,
                 work_id: str):
        self.submission_repository = submission_repository
        self.work_service = work_service
        self.storage_service = storage_service
        self.user_id = user_id
        self.event_id = event_id
        self.work_id = work_id

    async def get_all_event_submissions(self, offset: int, limit: int) -> list[SubmissionResponseSchema]:
        submissions = await self.submission_repository.get_all_submissions_for_event(self.event_id, offset, limit)
        return list(map(SubmissionsService.__map_to_schema, submissions))

    async def do_submit(self) -> SubmissionUploadSchema:
        await self.work_service.validate_update_work(self.work_id)
        my_work = await self.work_service.get_work(self.work_id)
        if my_work.state == WorkStates.RE_SUBMIT:
            submission_id = await self.submission_repository.do_new_submit(self.event_id, self.work_id)
        else:
            last_submission = await self.submission_repository.get_last_submission(self.event_id, self.work_id)
            if last_submission is None:
                submission_id = await self.submission_repository.do_new_submit(self.event_id, self.work_id)
            else:
                submission_id = await self.submission_repository.update_submit(last_submission.id)
        upload_url = await self.storage_service.get_submission_upload_url(self.event_id, self.work_id, submission_id)
        return SubmissionUploadSchema(
            id=submission_id,
            event_id=self.event_id,
            work_id=self.work_id,
            upload_url=upload_url
        )

    async def get_submission(self, submission_id: str) -> SubmissionDownloadSchema:
        return await self.__get_submission(submission_id)

    async def get_my_latest_submission(self) -> SubmissionDownloadSchema:
        last_submission = await self.submission_repository.get_last_submission(self.event_id, self.work_id)
        return await self.__get_submission(str(last_submission.id))

    async def __get_submission(self, submission_id: str) -> SubmissionDownloadSchema:
        download_url = await self.storage_service.get_submission_read_url(self.event_id, self.work_id, submission_id)
        return SubmissionDownloadSchema(
            id=submission_id,
            event_id=self.event_id,
            work_id=self.work_id,
            download_url=download_url
        )

    @staticmethod
    def __map_to_schema(model: SubmissionModel) -> SubmissionResponseSchema:
        return SubmissionResponseSchema(
            id=model.id,
            work_id=model.work_id,
            event_id=model.event_id,
        )
