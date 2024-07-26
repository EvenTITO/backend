from fastapi import APIRouter
from app.repository import events_crud
from app.database.dependencies import SessionDep
from app.organizers.dependencies import EventOrganizerDep
from app.events.utils import get_event
from app.events.schemas import ReviewSkeletonSchema

review_skeleton_configuration_router = APIRouter(prefix="/review-skeleton")


@review_skeleton_configuration_router.put("", status_code=204, response_model=None)
async def change_review_skeleton(
    _: EventOrganizerDep,
    event_id: str,
    review_skeleton: ReviewSkeletonSchema,
    db: SessionDep
):
    event = await get_event(db, event_id)
    await events_crud.update_review_skeleton(db, event, review_skeleton)
