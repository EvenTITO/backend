from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.utils import DateTemplate
from app.database.models.work import WorkModel


class SubmissionModel(DateTemplate, Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String, primary_key=True)
    work_id = Column(Integer, primary_key=True)

    # This is a Compose Foreign Key constraint: the submission references a
    # single work with id (event_id, work_id).
    # This is not the same as two single foreign keys for event_id and work_id.
    __table_args__ = (
        ForeignKeyConstraint(
            [event_id, work_id],
            [WorkModel.event_id, WorkModel.id],
            name="fk_work_from_submission"
        ),
        {}
    )

# TODO: revisar si en los requests que se hacen se esta trayendo todo por estas relationships o la carga es lazy
    work = relationship("WorkModel", back_populates="submissions")
    reviews = relationship("ReviewModel", back_populates="submission")
