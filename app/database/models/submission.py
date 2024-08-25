from sqlalchemy import (
    Column,
    String,
    Index, ForeignKey, )

from app.database.models.base import Base
from app.database.models.utils import ModelTemplate


class SubmissionModel(ModelTemplate, Base):
    __tablename__ = "submissions"

    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    work_id = Column(String, ForeignKey("works.id"), nullable=False)

    # This is a Compose Foreign Key constraint: the submission references a
    # single work with id (event_id, work_id).
    # This is not the same as two single foreign keys for event_id and work_id.
    __table_args__ = (
        Index('ix_submission_event_id', 'event_id'),
        Index('ix_submission_work_id', 'work_id'),
    )
