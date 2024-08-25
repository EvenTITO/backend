from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    UniqueConstraint,
    Integer,
    DateTime,
    ARRAY,
    JSON,
)
from sqlalchemy.orm import relationship
from app.database.models.base import Base
import enum

from app.database.models.utils import DateTemplate


class WorkStates(str, enum.Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RE_SUBMIT = "RE_SUBMIT"
    IN_REVISION = "IN_REVISION"
    SUBMITTED = "SUBMITTED"


class WorkModel(DateTemplate, Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), primary_key=True)

    title = Column(String, nullable=False)
    track = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    keywords = Column(ARRAY(String), nullable=False)
    authors = Column(JSON, nullable=False)

    state = Column(String, nullable=False, default=WorkStates.SUBMITTED)
    deadline_date = Column(DateTime, nullable=False)

    author_id = Column(String, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('event_id', 'title', name='event_id_title_uc'),
    )

    author = relationship(
        "UserModel",
        foreign_keys=[author_id],
        back_populates="works_as_author"
    )
    event = relationship("EventModel", foreign_keys=[event_id], back_populates="works")
    submissions = relationship("SubmissionModel", back_populates="work")
    reviewers = relationship("ReviewerModel", back_populates="work")
