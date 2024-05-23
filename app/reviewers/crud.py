from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from .model import ReviewerModel
from .schemas import ReviewerSchema


EVENT_REVIEWER_NOT_FOUND = "Event reviewer not found."


def handle_database_reviewer_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(
                status_code=404, detail=EVENT_REVIEWER_NOT_FOUND
            )

    return wrapper


def is_reviewer(
    db: Session, event_id: str, caller_id: str
):
    return db \
        .query(ReviewerModel) \
        .filter(
            ReviewerModel.id_event == event_id,
            ReviewerModel.id_reviewer == caller_id
        ).first() is not None


@handle_database_reviewer_error
def add_reviewer_to_event(
    db: Session, new_reviewer: ReviewerSchema
):
    new_reviewer = ReviewerModel(**new_reviewer.model_dump())
    db.add(new_reviewer)
    db.commit()
    db.refresh(new_reviewer)

    return new_reviewer


@handle_database_reviewer_error
def get_reviewer_in_event(db: Session, event_id: str, reviewer_id: str):
    return (
        db
        .query(ReviewerModel)
        .filter(
            ReviewerModel.id_event == event_id,
            ReviewerModel.id_reviewer == reviewer_id
        ).one()
    )


@handle_database_reviewer_error
def get_reviewers_in_event(db: Session, event_id: str):
    return (
        db
        .query(ReviewerModel)
        .filter(
            ReviewerModel.id_event == event_id
        ).all()
    )


@handle_database_reviewer_error
def get_user_event_assigned_reviews(db: Session, user_id: str):
    return (
        db
        .query(ReviewerModel)
        .filter(
            ReviewerModel.id_reviewer == user_id
        ).all()
    )


@handle_database_reviewer_error
def delete_reviewer(
    db: Session, reviewer_to_delete: ReviewerSchema
):
    reviewer = get_reviewer_in_event(
        db,
        reviewer_to_delete.id_event,
        reviewer_to_delete.id_reviewer
    )
    db.delete(reviewer)
    db.commit()
    return reviewer
