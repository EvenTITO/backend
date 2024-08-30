from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.repository.repository import get_repository
from app.repository.reviews_repository import ReviewsRepository
from app.services.event_reviews.event_reviews_service import EventReviewsService


class EventReviewsServiceChecker:
    async def __call__(
            self,
            event_id: UUID,
            work_id: UUID,
            reviews_repository: ReviewsRepository = Depends(get_repository(ReviewsRepository)),
    ) -> EventReviewsService:
        return EventReviewsService(event_id, work_id, reviews_repository)


event_reviews_checker = EventReviewsServiceChecker()
EventReviewsServiceDep = Annotated[EventReviewsService, Depends(event_reviews_checker)]
