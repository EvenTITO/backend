from enum import Enum
from sqlalchemy import Column, String
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.utils.models_utils import ModelTemplate


class UserPermission(str, Enum):
    ADMIN = "ADMIN"
    EVENT_CREATOR = "EVENT_CREATOR"
    NO_PERMISSION = "NO_PERMISSION"


class UserModel(ModelTemplate, Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    role = Column(String, default=UserPermission.NO_PERMISSION.value)

    events = relationship("EventModel", back_populates="creator")
    suscriptions = relationship(
        "SuscriptionModel", back_populates="suscriptor"
    )
    organizers = relationship(
        "OrganizerModel", back_populates="organizer"
    )

    def __repr__(self):
        return f"User({self.id})"
