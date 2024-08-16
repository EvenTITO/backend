from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKeyConstraint, Index, )
from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.utils import DateTemplate
from app.database.models.work import WorkModel


class SubmissionModel(DateTemplate, Base):
    __tablename__ = "submissions"

    # TODO revisar que se autogenere con 1 y luego 2 y asi sucesivamente
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String, nullable=False)
    work_id = Column(Integer, nullable=False)

    work = relationship("WorkModel", back_populates="submissions")
    reviews = relationship("ReviewModel", back_populates="submission")
    # TODO: revisar si en los requests que se hacen se esta trayendo todo por estas relationships o la carga es lazy

    # This is a Compose Foreign Key constraint: the submission references a
    # single work with id (event_id, work_id).
    # This is not the same as two single foreign keys for event_id and work_id.
    __table_args__ = (
        Index('ix_submission_event_id', 'event_id'),
        Index('ix_submission_work_id', 'work_id'),
        ForeignKeyConstraint(
            [event_id, work_id],
            [WorkModel.event_id, WorkModel.id],
            name="fk_work_from_submission"
        ),
    )
