from enum import Enum
from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.utils.models_utils import ModelTemplate


class OrganizerModel(ModelTemplate, Base):
    __tablename__ = "organizers"

    id_organizer = Column(String, ForeignKey("users.id"))
    id_event = Column(String, ForeignKey("events.id"))

    organizer = relationship("UserModel", back_populates="organizers")
    event = relationship("EventModel", back_populates="organizers")
