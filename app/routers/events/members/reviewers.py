from typing import List
from uuid import UUID

from fastapi import APIRouter, Query

from app.authorization.admin_user_dep import IsAdminUsrDep
from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.organizer_dep import IsOrganizerDep
from app.authorization.reviewer_dep import IsReviewerDep
from app.authorization.util_dep import or_
from app.schemas.members.reviewer_schema import ReviewerWithWorksResponseSchema, ReviewerCreateRequestSchema, \
    ReviewerAssignmentSchema, ReviewerWithWorksDeadlineResponseSchema
from app.schemas.users.utils import UID
from app.services.event_reviewers.event_reviewers_service_dep import EventReviewerServiceDep

event_reviewers_router = APIRouter(
    prefix="/{event_id}/reviewers",
    tags=["Events: Reviewers"]
)


@event_reviewers_router.post(
    path="",
    status_code=201,
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def add_reviewers(
        reviewers: ReviewerCreateRequestSchema,
        reviewer_service: EventReviewerServiceDep
) -> None:
    return await reviewer_service.add_reviewers(reviewers)


@event_reviewers_router.get(
    path="",
    response_model=List[ReviewerWithWorksDeadlineResponseSchema],
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def read_event_reviewers(
        reviewer_service: EventReviewerServiceDep,
        work_id: UUID = Query(default=None),
) -> List[ReviewerWithWorksResponseSchema]:
    return await reviewer_service.get_reviewers(work_id)


@event_reviewers_router.get(
    path="/my-assignments",
    response_model=list[ReviewerAssignmentSchema],
    dependencies=[or_(IsOrganizerDep, IsReviewerDep, IsAdminUsrDep)]
)
async def get_my_assignments(
        user_id: CallerIdDep,
        reviewer_service: EventReviewerServiceDep,
) -> list[ReviewerAssignmentSchema]:
    return await reviewer_service.get_my_assignments(user_id)


@event_reviewers_router.get(
    path="/{user_id}",
    response_model=ReviewerWithWorksResponseSchema,
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def read_event_reviewer_by_user(
        user_id: UID,
        reviewer_service: EventReviewerServiceDep,
) -> ReviewerWithWorksResponseSchema:
    return await reviewer_service.get_reviewer_by_user_id(user_id)
