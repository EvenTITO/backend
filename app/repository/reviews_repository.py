from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.review import ReviewModel
from app.repository.crud_repository import Repository
from app.schemas.users.utils import UID
from app.schemas.works.review import ReviewResponseSchema, ReviewCreateRequestSchema


class ReviewsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ReviewModel)

    async def get_all_work_reviews_for_event(
            self,
            event_id: UUID,
            work_id: UUID,
            offset: int,
            limit: int
    ) -> list[ReviewResponseSchema]:
        res = await self._get_many_with_conditions(
            [ReviewModel.event_id == event_id, ReviewModel.work_id == work_id],
            limit,
            offset
        )
        return [
            ReviewResponseSchema(
                id=row.id,
                event_id=row.event_id,
                work_id=row.work_id,
                submission_id=row.submission_id,
                reviewer_id=row.reviewer_id,
                status=row.status,
                review=row.review
            ) for row in res
        ]

    async def create_review(
            self,
            event_id: UUID,
            work_id: UUID,
            reviewer_id: UID,
            submission_id: UUID,
            review_schema: ReviewCreateRequestSchema
    ) -> ReviewResponseSchema:
        new_review = ReviewModel(
            event_id=event_id,
            work_id=work_id,
            reviewer_id=reviewer_id,
            submission_id=submission_id,
            status=review_schema.status,
            review=review_schema.review
        )
        saved_review = (await self._create(new_review))
        return ReviewResponseSchema(**saved_review.model_dump())
