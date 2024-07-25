from typing import List
from fastapi import APIRouter
from app.database.dependencies import SessionDep
from app.organizers.dependencies import EventOrganizerDep
from app.repository import reviewers_crud as crud
from app.events import validations
from app.reviewers.schemas.reviewer import (
    ReviewerSchema,
    ReviewerSchemaComplete
)

reviewers_router = APIRouter(
    prefix="/events/{event_id}/reviewers",
    tags=["Reviewers"]
)


@reviewers_router.post("/{user_id}", status_code=201)
async def create_reviewer(
        event_id: str,
        user_id: str,
        reviewer: ReviewerSchema,
        _: EventOrganizerDep,
        db: SessionDep
):
    await validations.validate_unique_reviewer(db, event_id, user_id)

    reviewer_created = await crud.create_reviewer(
        db=db,
        reviewer=reviewer,
        event_id=event_id,
        user_id=user_id
    )
    return reviewer_created


@reviewers_router.get(
    "",
    response_model=List[ReviewerSchemaComplete])
async def get_reviewer(
        event_id: str,
        db: SessionDep,
        _: EventOrganizerDep
):
    return await crud.get_all_reviewer(db, event_id)
