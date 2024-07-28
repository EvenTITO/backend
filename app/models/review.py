from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    JSON,
    ForeignKeyConstraint
)
from enum import Enum
from app.database.database import Base
from app.models.submission import SubmissionModel


class ReviewStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RE_SUBMIT = "RE_SUBMIT"
    PENDING = "PENDING"


class ReviewModel(Base):
    __tablename__ = "reviews"

    id_event = Column(String, primary_key=True)
    id_work = Column(Integer, primary_key=True)
    id_submission = Column(Integer, primary_key=True)

    id_reviewer = Column(String, ForeignKey("users.id"), primary_key=True)

    review = Column(JSON)
    review_status = Column(Enum(ReviewStatus), nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(
            [
                id_event,
                id_work,
                id_submission
            ],
            [
                SubmissionModel.id_event,
                SubmissionModel.id_work,
                SubmissionModel.id,
            ],
            name="fk_submission_from_review"
        ),
        {}
    )

    submission = relationship("SubmissionModel", back_populates="reviews")
    reviewer = relationship("UserModel", back_populates="reviews")
