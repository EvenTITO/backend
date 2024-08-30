from fastapi import APIRouter, Query

from app.authorization.admin_user_dep import IsAdminUsrDep
from app.authorization.organizer_dep import IsOrganizerDep
from app.authorization.reviewer_dep import IsWorkReviewerDep
from app.authorization.util_dep import or_
from app.schemas.works.review import ReviewResponseSchema, ReviewUploadSchema, ReviewCreateRequestSchema
from app.services.event_reviews.event_reviews_service_dep import EventReviewsServiceDep

reviews_router = APIRouter(prefix="/events/{event_id}/works/{work_id}/reviews", tags=["Event: Works Reviews"])


@reviews_router.get(
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


@reviews_router.post(
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


"""

@reviews_router.patch("/status")
async def update_work_review_status():
    #The organizer uses this method to update the review status that the author will later see.
    pass


@reviews_router.put("/{review_id}")
async def update_review(review_id: UUID):
    #The reviewer uses this method to update his review.
    pass


@reviews_router.get("")
async def get_all_works_assigned_for_my_review():
    #This method is used by a reviewer to get all his asigned works.
    pass


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
