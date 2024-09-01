from uuid import UUID

from app.database.models.work import WorkStates
from app.exceptions.reviews_exceptions import IsNotWorkRevisionPeriod
from app.repository.reviews_repository import ReviewsRepository
from app.schemas.users.utils import UID
from app.schemas.works.review import ReviewUploadSchema, ReviewCreateRequestSchema, ReviewResponseSchema
from app.services.event_submissions.event_submissions_service import SubmissionsService
from app.services.services import BaseService
from app.services.storage.work_storage_service import WorkStorageService
from app.services.works.works_service import WorksService


class EventReviewsService(BaseService):
    def __init__(
            self,
            event_id: UUID,
            work_id: UUID,
            caller_id: UID,
            work_service: WorksService,
            submission_service: SubmissionsService,
            storage_service: WorkStorageService,
            reviews_repository: ReviewsRepository,
    ):
        self.event_id = event_id
        self.work_id = work_id
        self.caller_id = caller_id
        self.work_service = work_service
        self.submission_service = submission_service
        self.storage_service = storage_service
        self.reviews_repository = reviews_repository

    async def get_all_reviews(self, offset: int, limit: int) -> list[ReviewResponseSchema]:
        return await self.reviews_repository.get_all_work_reviews_for_event(self.event_id, self.work_id, offset, limit)

    async def add_review(self, review_schema: ReviewCreateRequestSchema) -> ReviewUploadSchema:
        my_work = await self.work_service.get_work(self.work_id)
        if my_work.state != WorkStates.IN_REVISION:
            raise IsNotWorkRevisionPeriod(self.event_id, self.work_id)

        last_submission = await self.submission_service.get_latest_submission()

        saved_review = await self.reviews_repository.create_review(
            self.event_id,
            self.work_id,
            self.caller_id,
            last_submission.id,
            review_schema
        )
        upload_url = await self.storage_service.get_review_upload_url(saved_review.id)
        return ReviewUploadSchema(**saved_review.model_dump(), upload_url=upload_url)

    async def update_review(self, review_id: UUID, review_schema: ReviewCreateRequestSchema) -> None:
        my_work = await self.work_service.get_work(self.work_id)
        if my_work.state != WorkStates.IN_REVISION:
            raise IsNotWorkRevisionPeriod(self.event_id, self.work_id)

        await self.reviews_repository.update_review(review_id, review_schema)
