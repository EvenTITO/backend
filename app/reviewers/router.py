from typing import List
from app.utils.dependencies import SessionDep, CallerIdDep
from app.reviewers import crud
from .schemas import ReviewerRequestSchema, ReviewerSchema
from fastapi import APIRouter
from app.users.router import users_router
from app.events.router import events_router
from app.utils.authorization import (
    validate_reviewer_permissions,
    validate_same_user_or_superuser
)


reviewers_events_router = APIRouter(
    prefix=events_router.prefix+"/{event_id}"+'/reviewers',
    tags=["Event Reviewers"]
)

reviewers_users_router = APIRouter(
    prefix=users_router.prefix+"/{user_id}"+'/assigned-reviews',
    tags=["User Reviewers"]
)


@reviewers_events_router.post("", status_code=201)
def create_reviewer(
    event_id: str,
    reviewer: ReviewerRequestSchema,
    caller_id: CallerIdDep,
    db: SessionDep
) -> str:
    validate_reviewer_permissions(db, event_id, caller_id)

    reviewer = crud.add_reviewer_to_event(
        db,
        ReviewerSchema(
            **reviewer.model_dump(),
            id_event=event_id
        )
    )
    return reviewer.id_reviewer


@reviewers_events_router.get(
    "", response_model=List[ReviewerSchema]
)
def read_event_reviewers(
    event_id: str,
    caller_id: CallerIdDep,
    db: SessionDep
):
    validate_reviewer_permissions(db, event_id, caller_id)
    return crud.get_reviewers_in_event(db, event_id)


@reviewers_users_router.get(
    "", response_model=List[ReviewerSchema]
)
def read_user_event_assigned_reviews(
    user_id: str,
    caller_id: CallerIdDep,
    db: SessionDep
):
    validate_same_user_or_superuser(db, user_id, caller_id)
    return crud.get_user_event_assigned_reviews(db, user_id)


@reviewers_events_router.delete(
    "/{reviewer_id}",
    status_code=204
)
def delete_reviewer(
    event_id: str,
    reviewer_id: str,
    caller_id: CallerIdDep,
    db: SessionDep
):
    validate_reviewer_permissions(db, event_id, caller_id)
    reviewer = ReviewerSchema(
        id_reviewer=reviewer_id,
        id_event=event_id
    )

    crud.delete_reviewer(
        db, reviewer
    )
