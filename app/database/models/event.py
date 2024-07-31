from sqlalchemy import Column, String, ForeignKey, JSON, ARRAY
from app.database.database import Base
from app.database.models.utils import ModelTemplate
from enum import Enum
from sqlalchemy.orm import relationship


class EventStatus(str, Enum):
    WAITING_APPROVAL = "WAITING_APPROVAL"
    NOT_APPROVED = "NOT_APPROVED"
    CREATED = "CREATED"
    STARTED = "STARTED"
    SUSPENDED = "SUSPENDED"
    CANCELED = "CANCELED"
    BLOCKED = "BLOCKED"


class EventType(str, Enum):
    CONFERENCE = "CONFERENCE"
    TALK = "TALK"


class EventModel(ModelTemplate, Base):
    __tablename__ = "events"

    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    event_type = Column(String)
    status = Column(String, default=EventStatus.WAITING_APPROVAL)
    creator_id = Column(String, ForeignKey("users.id"))
    location = Column(String)
    tracks = Column(ARRAY(String))

    notification_mails = Column(ARRAY(String))

    review_skeleton = Column(JSON, default=None)
    pricing = Column(JSON, default=None)
    dates = Column(JSON)

    contact = Column(String, nullable=True)
    organized_by = Column(String, nullable=True)
    media = Column(ARRAY(JSON), default=None)

    creator = relationship("UserModel", foreign_keys=[creator_id], back_populates="events")
    inscriptions = relationship("InscriptionModel", back_populates="event")
    organizers = relationship("OrganizerModel", back_populates="event")
    chairs = relationship("ChairModel", back_populates="event")
    works = relationship("WorkModel", back_populates="event")
