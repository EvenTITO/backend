from app.database.models.reviewer import ReviewerModel
from app.database.models.user import UserModel
from app.exceptions.members.reviewer.reviewer_exceptions import UserNotIsReviewer
from app.repository.reviewers_repository import ReviewerRepository
from app.repository.users_repository import UsersRepository
from app.schemas.members.reviewer_schema import ReviewerResponseSchema
from app.schemas.users.user import UserSchema
from app.services.events.events_service import EventsService
from app.services.services import BaseService


class EventReviewerService(BaseService):
    def __init__(
            self,
            event_service: EventsService,
            reviewer_repository: ReviewerRepository,
            users_repository: UsersRepository
    ):
        self.event_service = event_service
        self.reviewer_repository = reviewer_repository
        self.users_repository = users_repository

    async def get_all_reviewers(self, event_id: str):
        users_reviewers = await self.reviewer_repository.get_all(event_id)
        return list(map(EventReviewerService.__map_to_schema, users_reviewers))

    async def get_reviewer(self, event_id: str, user_id: str):
        if not await self.reviewer_repository.is_member(event_id, user_id):
            raise UserNotIsReviewer(event_id, user_id)
        chair = await self.reviewer_repository.get_member(event_id, user_id)
        return EventReviewerService.__map_to_schema(chair)

    async def remove_reviewer(self, event_id: str, user_id: str) -> None:
        if not await self.reviewer_repository.is_member(event_id, user_id):
            raise UserNotIsReviewer(event_id, user_id)
        await self.reviewer_repository.remove_member(event_id, user_id)

    async def is_reviewer(self, event_id: str, user_id: str) -> None:
        return await self.reviewer_repository.is_member(event_id, user_id)

    @staticmethod
    def __map_to_schema(model: (UserModel, ReviewerModel)) -> ReviewerResponseSchema:
        user, reviewer = model
        return ReviewerResponseSchema(
            event_id=reviewer.event_id,
            user_id=reviewer.user_id,
            user=UserSchema(
                email=user.email,
                name=user.name,
                lastname=user.lastname
            )
        )
