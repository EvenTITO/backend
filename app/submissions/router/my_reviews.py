from fastapi import APIRouter
from app.submissions.schemas.work import BasicWorkInfo

my_reviews_router = APIRouter(
    prefix="/events/{event_id}/my-reviews",
    tags=["Reviews"]
)


@my_reviews_router.get("")
async def get_all_works_assigned_for_my_review() -> list[BasicWorkInfo]:
    """
    This method is used by a reviewer to get all his asigned works.
    """
    pass
