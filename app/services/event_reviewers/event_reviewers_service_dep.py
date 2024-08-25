from typing import Annotated

from fastapi import Depends

from app.repository.repository import get_repository
from app.repository.reviewers_repository import ReviewerRepository
from app.repository.users_repository import UsersRepository
from app.services.event_reviewers.event_reviewers_service import EventReviewerService
from app.services.events.events_service_dep import EventsServiceDep


class EventsReviewerChecker:
    async def __call__(
            self,
            events_service: EventsServiceDep,
            users_repository: UsersRepository = Depends(get_repository(UsersRepository)),
            reviewer_repository: ReviewerRepository = Depends(get_repository(ReviewerRepository)),
    ) -> EventReviewerService:
        return EventReviewerService(events_service, reviewer_repository, users_repository)


event_reviewer_checker = EventsReviewerChecker()
EventChairServiceDep = Annotated[EventReviewerService, Depends(event_reviewer_checker)]
