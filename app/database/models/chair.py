from enum import Enum

from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.database.models.utils import DateTemplate


# TODO duplicado con organizer, mejorar esto
class InvitationStatus(str, Enum):
    INVITED = "INVITED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ChairModel(DateTemplate, Base):
    __tablename__ = "chairs"

    id_chair = Column(String, primary_key=True)
    id_event = Column(String, primary_key=True)

    invitation_expiration_date = Column(Date)
    invitation_status = Column(String, nullable=False)
    tracks = Column(String)

    chair = relationship("UserModel", back_populates="chairs")
    event = relationship("EventModel", back_populates="chairs")
