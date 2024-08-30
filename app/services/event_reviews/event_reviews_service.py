from uuid import UUID

from app.repository.reviews_repository import ReviewsRepository
from app.services.services import BaseService


class EventReviewsService(BaseService):
    def __init__(
            self,
            event_id: UUID,
            work_id: UUID,
            reviews_repository: ReviewsRepository,
    ):
        self.event_id = event_id
        self.work_id = work_id
        self.reviews_repository = reviews_repository

    async def get_all_reviews(self, offset: int, limit: int):
        return await self.reviews_repository.get_all_work_reviews_for_event(self.event_id, self.work_id, offset, limit)
