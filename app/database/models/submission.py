from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKeyConstraint,
    Boolean
)
from sqlalchemy.orm import relationship
from app.database.models.base import Base
from app.database.models.work import WorkModel


class SubmissionModel(Base):
    __tablename__ = "submissions"

    event_id = Column(String, primary_key=True)
    work_id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True)

    review_decision = Column(String, nullable=True)
    review_comments = Column(String, nullable=True)
    public_review = Column(Boolean, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            [event_id, work_id],
            [WorkModel.event_id, WorkModel.id],
            name="fk_work_from_submission"
        ),
        {}
    )

    work = relationship("WorkModel", back_populates="submissions")
    reviews = relationship("ReviewModel", back_populates="submission")
