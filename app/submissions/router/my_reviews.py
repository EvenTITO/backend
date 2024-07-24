from fastapi import APIRouter

reviews_router = APIRouter(
    prefix="/events/{event_id}/my-reviews",
    tags=["Reviews"]
)


@reviews_router.get("")
async def get_all_works_assigned_for_my_review():
    """
    This method is used by a reviewer to get all his asigned works.
    """
    pass
