from sqlalchemy import Column, String, Date, ForeignKey
from app.database.database import Base
from .models_utils import ModelTemplate
from enum import Enum
from sqlalchemy.orm import relationship


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

    def __repr__(self):
        return f"Event({self.id})"
