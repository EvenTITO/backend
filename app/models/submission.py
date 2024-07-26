from sqlalchemy import (
    Column,
    String,
    Integer,
    ARRAY,
    JSON,
    ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.work import WorkModel


class SubmissionModel(Base):
    __tablename__ = "submissions"

    id_event = Column(String, primary_key=True)
    id_work = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True)

    abstract = Column(String)
    keywords = Column(ARRAY(String), default='{}')
    authors = Column(JSON)

    review_decision = Column(String, nullable=True)
    review_comments = Column(String, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            [id_event, id_work],
            [WorkModel.id_event, WorkModel.id],
            name="fk_work_from_submission"
        ),
        {}
    )

    work = relationship("WorkModel", back_populates="submissions")
    reviews = relationship("ReviewModel", back_populates="submission")
