from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    UniqueConstraint,
    Integer,
    Date,
    ARRAY,
    JSON
)
from sqlalchemy.orm import relationship
from app.database.database import Base
from enum import Enum


class WorkStates(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RE_SUBMIT = "RE_SUBMIT"
    IN_REVISION = "IN_REVISION"
    SUBMITTED = "SUBMITTED"


class WorkModel(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True)
    id_event = Column(String, ForeignKey("events.id"), primary_key=True)

    title = Column(String, nullable=False)
    track = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    keywords = Column(ARRAY(String), nullable=False)
    authors = Column(JSON, nullable=False)

    state = Column(Enum(WorkStates), nullable=False, default=WorkStates.SUBMITTED)
    deadline_date = Column(Date, nullable=False)

    id_author = Column(String, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('id_event', 'title', name='event_id_title_uc'),
    )

    author = relationship(
        "UserModel",
        foreign_keys=[id_author],
        back_populates="works_as_author"
    )
    event = relationship("EventModel", back_populates="works")
    submissions = relationship("SubmissionModel", back_populates="work")
