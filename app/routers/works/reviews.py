from uuid import UUID

from fastapi import APIRouter, Query

from app.authorization.admin_user_dep import IsAdminUsrDep
from app.authorization.organizer_dep import IsOrganizerDep
from app.authorization.reviewer_dep import IsWorkReviewerDep
from app.authorization.util_dep import or_
from app.schemas.works.review import ReviewResponseSchema, ReviewUploadSchema, ReviewCreateRequestSchema
from app.services.event_reviews.event_reviews_service_dep import EventReviewsServiceDep

event_reviews_router = APIRouter(prefix="/{event_id}/works/{work_id}/reviews", tags=["Event: Works Reviews"])


@event_reviews_router.get(
    path="",
    status_code=200,
    response_model=list[ReviewResponseSchema],
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def get_all_reviews(
        reviews_service: EventReviewsServiceDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100)
) -> list[ReviewResponseSchema]:
    return await reviews_service.get_all_reviews(offset, limit)


@event_reviews_router.post(
    path="",
    status_code=201,
    response_model=ReviewUploadSchema,
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep, IsWorkReviewerDep)]
)
async def add_review(
        review_schema: ReviewCreateRequestSchema,
        reviews_service: EventReviewsServiceDep
) -> ReviewUploadSchema:
    return await reviews_service.add_review(review_schema)


@event_reviews_router.put(
    path="/{review_id}",
    status_code=201,
    response_model=None,
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep, IsWorkReviewerDep)]
)
async def update_review(
        review_id: UUID,
        review_schema: ReviewCreateRequestSchema,
        reviews_service: EventReviewsServiceDep
) -> None:
    return await reviews_service.update_review(review_id, review_schema)


#TODO
"""


@reviews_router.post("/publish", status_code=204)
async def publish_reviews_to_authors(reviews_to_publish: PublishReviews):
    #The organizer uses this method to publish the reviews to the authors.

    {

        "reviews_to_publish": list[str]
        new_work_status: WORK_STATE(resubmit, rejected, accept)
        fecha reentrega
    }
    pass
"""
