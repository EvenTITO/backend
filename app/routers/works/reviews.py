from fastapi import APIRouter

reviews_router = APIRouter(prefix="/events/{event_id}/works/{work_id}/reviews", tags=["Event: Works Reviews"])


@reviews_router.get("")
async def get_all_the_work_information_for_reviewing():
    """
    Obtain the Work with all it's information including all the
    reviews made by the reviewers.
    The user must be a reviewer for this work or an event organizer
    """
    pass


@reviews_router.post("")
async def add_a_review():
    """
    The reviewer uses this method to submit a review.
    """
    pass


@reviews_router.patch("/status")
async def update_work_review_status():
    """
    The organizer uses this method to update the
    review status that the author will later see.
    """
    pass


@reviews_router.put("/{review_id}")
async def update_review(review_id: int):
    """
    The reviewer uses this method to update his review.
    """
    pass


@reviews_router.get("")
async def get_all_works_assigned_for_my_review():
    """
    This method is used by a reviewer to get all his asigned works.
    """
    pass
