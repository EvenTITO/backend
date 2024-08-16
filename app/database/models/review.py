import enum

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    JSON,
    ForeignKeyConstraint
)
from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.submission import SubmissionModel


class ReviewStatus(str, enum.Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RE_SUBMIT = "RE_SUBMIT"
    PENDING = "PENDING"


class ReviewModel(Base):
    __tablename__ = "reviews"

    event_id = Column(String, primary_key=True)
    work_id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, primary_key=True)
    reviewer_id = Column(String, ForeignKey("users.id"), primary_key=True)

    review = Column(JSON)
    review_status = Column(String, nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(
            [submission_id],
            [SubmissionModel.id],
            name="fk_submission_from_review"
        ),
    )

    submission = relationship("SubmissionModel", back_populates="reviews")
    reviewer = relationship("UserModel", back_populates="reviews")
