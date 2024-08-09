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
        # todo -> falta validar el estado para ver si es una submission nueva o no y actualizar la fecha
        submission_id = await self.submission_repository.do_submit(self.event_id, self.work_id)
        upload_url = await self.storage_service.get_submission_upload_url(self.event_id, self.work_id, submission_id)
        return SubmissionSchema(id=submission_id, upload_url=upload_url)
