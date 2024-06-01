from enum import Enum
from sqlalchemy import Column, String
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.utils.models_utils import ModelTemplate


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    EVENT_CREATOR = "EVENT_CREATOR"
    DEFAULT = "DEFAULT"


class UserModel(ModelTemplate, Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    role = Column(String, default=UserRole.DEFAULT.value)

    events = relationship("EventModel", back_populates="creator")
    inscriptions = relationship(
        "InscriptionModel",
        back_populates="inscriptor"
    )
    organizers = relationship(
        "OrganizerModel",
        back_populates="organizer"
    )

    def __repr__(self):
        return f"User({self.id})"
