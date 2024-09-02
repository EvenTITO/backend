from uuid import UUID

from sqlalchemy import update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.review import ReviewModel
from app.database.models.submission import SubmissionModel
from app.database.models.work import WorkModel
from app.repository.crud_repository import Repository
from app.schemas.users.utils import UID
from app.schemas.works.review import ReviewResponseSchema, ReviewCreateRequestSchema, ReviewPublishSchema


class ReviewsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ReviewModel)

    async def get_all_work_reviews_for_event(
            self, event_id: UUID, work_id: UUID, offset: int, limit: int) -> list[ReviewResponseSchema]:
        return await self._get_work_reviews(
            [ReviewModel.event_id == event_id, ReviewModel.work_id == work_id],
            offset,
            limit
        )

    async def get_shared_work_reviews(
            self, event_id: UUID, work_id: UUID, offset: int, limit: int) -> list[ReviewResponseSchema]:
        return await self._get_work_reviews(
            [ReviewModel.event_id == event_id, ReviewModel.work_id == work_id, ReviewModel.shared.is_(True)],
            offset,
            limit
        )

    async def create_review(
            self,
            event_id: UUID,
            work_id: UUID,
            reviewer_id: UID,
            submission_id: UUID,
            review_schema: ReviewCreateRequestSchema
    ) -> ReviewResponseSchema:
        new_review = ReviewModel(
            **review_schema.model_dump(),
            event_id=event_id,
            work_id=work_id,
            reviewer_id=reviewer_id,
            submission_id=submission_id
        )
        saved_review = (await self._create(new_review))
        return ReviewResponseSchema(
            id=saved_review.id,
            event_id=saved_review.event_id,
            work_id=saved_review.work_id,
            submission_id=saved_review.submission_id,
            reviewer_id=saved_review.reviewer_id,
            review=saved_review.review,
            status=saved_review.status,
        )

    async def update_review(self, review_id: UUID, review_update: ReviewCreateRequestSchema) -> bool:
        conditions = [ReviewModel.id == review_id]
        return await self._update_with_conditions(conditions, review_update)

    async def publish_reviews(self, event_id: UUID, work_id: UUID, reviews_to_publish: ReviewPublishSchema) -> bool:
        reviews_ids = reviews_to_publish.reviews_to_publish
        if len(reviews_ids) == 0:
            return False
        update_work_query = (
            update(WorkModel)
            .where(and_(WorkModel.event_id == event_id, WorkModel.id == work_id))
            .values(state=reviews_to_publish.new_work_status, deadline_date=reviews_to_publish.resend_deadline)
        )
        for review_id in reviews_ids:
            conditions = [
                ReviewModel.event_id == event_id,
                ReviewModel.work_id == work_id,
                ReviewModel.id == review_id
            ]
            review = await self._get_with_conditions(conditions)
            if not review:
                return False

            update_review_query = (
                update(ReviewModel)
                .where(ReviewModel.id == review.id)
                .values(shared=True)
            )
            update_submission_query = (
                update(SubmissionModel)
                .where(SubmissionModel.id == review.submission_id)
                .values(state=reviews_to_publish.new_work_status)
            )
            await self.session.execute(update_review_query)
            await self.session.execute(update_submission_query)
        await self.session.execute(update_work_query)
        await self.session.commit()
        return True

    async def _get_work_reviews(
            self,
            conditions,
            offset: int,
            limit: int
    ) -> list[ReviewResponseSchema]:
        res = await self._get_many_with_conditions(conditions, offset, limit)
        return [
            ReviewResponseSchema(
                id=row.id,
                event_id=row.event_id,
                work_id=row.work_id,
                submission_id=row.submission_id,
                reviewer_id=row.reviewer_id,
                status=row.status,
                review=row.review,
                shared=row.shared
            ) for row in res
        ]
