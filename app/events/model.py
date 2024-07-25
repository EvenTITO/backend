from datetime import datetime
from app.utils.exceptions import DatesException
from sqlalchemy import Column, String, Date, ForeignKey, JSON, ARRAY
from app.database.database import Base
from app.utils.models_utils import ModelTemplate
from enum import Enum
from sqlalchemy.orm import relationship, validates


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
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)
    event_type = Column(String)
    status = Column(String, default=EventStatus.WAITING_APPROVAL)
    id_creator = Column(String, ForeignKey("users.id"))
    location = Column(String)
    tracks = Column(ARRAY(String))

    notification_mails = Column(ARRAY(String), default='{}')

    review_skeleton = Column(JSON, default=None)
    pricing = Column(JSON, default=None)
    dates = Column(JSON, default=None)

    contact = Column(String, nullable=True)
    organized_by = Column(String, nullable=True)
    media = Column(ARRAY(JSON), default=None)

    creator = relationship("UserModel", back_populates="events")
    inscriptions = relationship("InscriptionModel", back_populates="event")
    organizers = relationship("OrganizerModel", back_populates="event")

    @validates("start_date")
    def validate_start_date(self, key, start_date):
        if start_date is None:
            return start_date
        if datetime.now() > start_date:
            raise DatesException()
        else:
            return start_date

    @validates("end_date")
    def validate_end_date(self, key, end_date):
        if end_date is None:
            return end_date
        if datetime.now() > end_date:
            raise DatesException()
        elif self.start_date and end_date <= self.start_date:
            raise DatesException()
        else:
            return end_date

    def __repr__(self):
        return f"Event({self.id})"


class EventModelRol:
    def __init__(self, eventModel, col_val):
        self.__dict__ = eventModel.__dict__.copy()
        self.rol = col_val
