from enum import Enum
from sqlalchemy import Column, String, ForeignKey, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.database.models.utils import DateTemplate


class InvitationStatus(str, Enum):
    INVITED = "INVITED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class OrganizerModel(DateTemplate, Base):
    __tablename__ = "organizers"

    organizer_id = Column(String, ForeignKey("users.id"), primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), primary_key=True)
    invitation_expiration_date = Column(DateTime, nullable=True)
    invitation_status = Column(String, default=InvitationStatus.INVITED.value)

    organizer = relationship("UserModel", back_populates="organizers")
    event = relationship("EventModel", back_populates="organizers")
