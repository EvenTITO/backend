from fastapi import APIRouter, Depends
from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.user_id_dep import verify_user_exists
from app.repository import events_crud
from app.database.session_dep import SessionDep
from app.organizers.dependencies import EventOrganizerDep
from app.events.utils import get_event
from app.schemas.events.review_skeleton.review_skeleton import ReviewSkeletonSchema

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


@review_skeleton_configuration_router.get("", status_code=200, dependencies=[Depends(verify_user_exists)])
async def get_review_skeleton(
        _: EventOrganizerDep,
        caller_id: CallerIdDep,
        event_id: str,
        db: SessionDep
) -> ReviewSkeletonSchema:
    return await events_crud.get_review_sckeletor(db, event_id, caller_id)
