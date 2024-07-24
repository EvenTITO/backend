from fastapi import APIRouter

my_works_router = APIRouter(
    prefix="/events/{event_id}/my-works",
    tags=["My Works"]
)


@my_works_router.get("")
async def get_my_works():
    """
    Get all my works for which I am the main author in the event.
    """
    pass
