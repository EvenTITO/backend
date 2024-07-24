from fastapi import APIRouter
from app.submissions.schemas.work import BasicWorkInfoForAuthor

my_works_router = APIRouter(
    prefix="/events/{event_id}/my-works",
    tags=["My Works"]
)


@my_works_router.get("")
async def get_my_works() -> list[BasicWorkInfoForAuthor]:
    """
    Get all my works for which I am the main author in the event.
    """
    pass
