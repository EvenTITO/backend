from app.submissions.schemas.review_management import (
    ReviewAssignment,
    PublishReviews
)
from fastapi import APIRouter

review_management_router = APIRouter(
    prefix="/events/{event_id}/reviews-management",
    tags=["Review Management"]
)


@review_management_router.patch("/assignments", status_code=204)
async def assign_a_work_to_a_reviewer(
    review_assignments: list[ReviewAssignment]
):
    """
    The organizer uses this method to assign
    the works to reviewers
    """
    pass


@review_management_router.post("/publish", status_code=204)
async def publish_reviews_to_authors(reviews_to_publish: PublishReviews):
    """
    The organizer uses this method to publish the reviews to
    the authors.
    """
    pass
