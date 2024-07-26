from app.models.submission import SubmissionModel
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    JSON,
    ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from app.database.database import Base


class ReviewModel(Base):
    __tablename__ = "reviews"

    id_event = Column(
        String,
        primary_key=True
    )
    id_work = Column(
        Integer,
        primary_key=True
    )
    id_submission = Column(
        Integer,
        primary_key=True
    )
    id_reviewer = Column(String, ForeignKey("users.id"), primary_key=True)

    review = Column(JSON)

    __table_args__ = (
        ForeignKeyConstraint(
            [
                id_event,
                id_work,
                id_submission],
            [
                SubmissionModel.id_event,
                SubmissionModel.id_work,
                SubmissionModel.id
            ],
            name="fk_submission_from_review"
        ),
        {}
    )

    submission = relationship("SubmissionModel", back_populates="reviews")
    reviewer = relationship("UserModel", back_populates="reviews")
