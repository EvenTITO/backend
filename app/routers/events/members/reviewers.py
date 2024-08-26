from typing import List

from fastapi import APIRouter, Query

from app.authorization.admin_user_dep import IsAdminUsrDep
from app.authorization.organizer_dep import IsOrganizerDep
from app.authorization.util_dep import or_
from app.schemas.members.reviewer_schema import ReviewerWithWorksResponseSchema, ReviewerCreateRequestSchema, \
    ReviewerResponseSchema
from app.services.event_reviewers.event_reviewers_service_dep import EventReviewerServiceDep

event_reviewers_router = APIRouter(
    prefix="/{event_id}/reviewers",
    tags=["Events: Reviewers"]
)

event_works_reviewers_router = APIRouter(
    prefix="/{event_id}/works/{work_id}/reviewers",
    tags=["Event: Works Reviewers"]
)


@event_reviewers_router.post(
    path="",
    status_code=201,
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def add_reviewers(
        event_id: str,
        reviewers: ReviewerCreateRequestSchema,
        reviewer_service: EventReviewerServiceDep
) -> None:
    return await reviewer_service.add_reviewers(event_id, reviewers)


@event_reviewers_router.get(
    path="",
    response_model=List[ReviewerWithWorksResponseSchema],
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def read_event_reviewers(
        reviewer_service: EventReviewerServiceDep,
        event_id: str,
        work_id: str = Query(default=None),
) -> List[ReviewerWithWorksResponseSchema]:
    return await reviewer_service.get_reviewers(event_id, work_id)


@event_reviewers_router.get(
    path="/{user_id}",
    response_model=ReviewerWithWorksResponseSchema,
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def read_event_reviewer_by_user(
        reviewer_service: EventReviewerServiceDep,
        event_id: str,
        user_id: str,
) -> ReviewerWithWorksResponseSchema:
    return await reviewer_service.get_reviewer_by_user_id(event_id, user_id)


@event_works_reviewers_router.get(
    path="/{user_id}",
    response_model=ReviewerResponseSchema,
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def read_event_reviewer_by_user_and_work(
        reviewer_service: EventReviewerServiceDep,
        event_id: str,
        work_id: str,
        user_id: str,
) -> ReviewerResponseSchema:
    return await reviewer_service.get_reviewer_by_user_id_and_work_id(event_id, user_id, work_id)
