from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.utils.models_utils import DateTemplate


class OrganizerModel(DateTemplate, Base):
    __tablename__ = "organizers"

    id_organizer = Column(String, ForeignKey("users.id"), primary_key=True)
    id_event = Column(String, ForeignKey("events.id"), primary_key=True)

    organizer = relationship("UserModel", back_populates="organizers")
    event = relationship("EventModel", back_populates="organizers")
