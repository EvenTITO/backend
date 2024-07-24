from fastapi import APIRouter

review_management_router = APIRouter(
    prefix="/events/{event_id}/reviews-management",
    tags=["Review Management"]
)


@review_management_router.patch("/assignments")
async def assign_a_work_to_a_reviewer():
    """
    The organizer uses this method to assign
    the works to reviewers
    """
    pass


@review_management_router.post("/publish")
async def publish_reviews_to_authors():
    """
    The organizer uses this method to publish the reviews to
    the authors.
    """
    pass
