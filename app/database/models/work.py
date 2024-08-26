import enum

from sqlalchemy import (
    UUID,
    Column,
    String,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    ARRAY,
    JSON,
)

from app.database.models.base import Base
from app.database.models.utils import ModelTemplate, UIDType


class WorkStates(str, enum.Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RE_SUBMIT = "RE_SUBMIT"
    IN_REVISION = "IN_REVISION"
    SUBMITTED = "SUBMITTED"


class WorkModel(ModelTemplate, Base):
    __tablename__ = "works"

    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    author_id = Column(UIDType, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)
    track = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    keywords = Column(ARRAY(String), nullable=False)
    authors = Column(JSON, nullable=False)
    state = Column(String, nullable=False, default=WorkStates.SUBMITTED)
    deadline_date = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint('event_id', 'title', name='event_id_title_uc'),
    )
