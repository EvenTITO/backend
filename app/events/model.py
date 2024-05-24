from datetime import datetime
from app.utils.exceptions import DatesException
from sqlalchemy import Column, String, Date, ForeignKey
from app.database.database import Base
from app.utils.models_utils import ModelTemplate
from enum import Enum
from sqlalchemy.orm import relationship, validates


class EventStatus(str, Enum):
    CREATED = "CREATED"
    STARTED = "STARTED"


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
    status = Column(String)
    id_creator = Column(String, ForeignKey("users.id"))

    creator = relationship("UserModel", back_populates="events")
    suscriptions = relationship("SuscriptionModel", back_populates="event")
    organizers = relationship("OrganizerModel", back_populates="event")

    @validates("start_date")
    def validate_start_date(self, key, start_date):
        if datetime.now() > start_date:
            raise DatesException()
        else:
            return start_date

    @validates("end_date")
    def validate_end_date(self, key, end_date):
        if datetime.now() > end_date:
            raise DatesException()
        elif self.start_date and end_date <= self.start_date:
            raise DatesException()
        else:
            return end_date

    def __repr__(self):
        return f"Event({self.id})"

    def to_dict(self):
        return {
            "id_event": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
