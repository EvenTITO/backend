import enum

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    JSON
)

from app.database.models.utils import DateTemplate


class ReviewStatus(str, enum.Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RE_SUBMIT = "RE_SUBMIT"
    PENDING = "PENDING"


class ReviewModel(DateTemplate):
    __tablename__ = "reviews"

    submission_id = Column(String, ForeignKey("submissions.id"), primary_key=True)
    reviewer_id = Column(String, ForeignKey("users.id"), primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    work_id = Column(String, ForeignKey("works.id"), nullable=False)

    review = Column(JSON)
    review_status = Column(String, nullable=False)
