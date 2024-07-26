from enum import Enum
from sqlalchemy import Column, String, ForeignKey, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.utils.models_utils import DateTemplate
from datetime import datetime, timedelta


class InvitationStatus(str, Enum):
    INVITED = "INVITED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class OrganizerModel(DateTemplate, Base):
    __tablename__ = "organizers"

    id_organizer = Column(String, ForeignKey("users.id"), primary_key=True)
    id_event = Column(String, ForeignKey("events.id"), primary_key=True)
    invitation_expiration_date = Column(
        DateTime,
        default=datetime.now()+timedelta(days=365),
        nullable=False
    )  # TODO: fix this to a function, now is static.
    invitation_status = Column(String, default=InvitationStatus.INVITED.value)

    organizer = relationship("UserModel", back_populates="organizers")
    event = relationship("EventModel", back_populates="organizers")
