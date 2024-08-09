from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.utils import DateTemplate


class SubmissionModel(DateTemplate, Base):
    __tablename__ = "submissions"

    event_id = Column(String, ForeignKey("events.id"), primary_key=True)
    work_id = Column(Integer, ForeignKey("works.id"), primary_key=True)
    id = Column(Integer, primary_key=True)

    work = relationship("WorkModel", foreign_keys=[work_id], back_populates="submissions")
    event = relationship("EventModel", foreign_keys=[event_id], back_populates="events")

