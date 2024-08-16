from enum import Enum
from sqlalchemy import Column, String
from app.database.models.base import Base
from sqlalchemy.orm import relationship
from app.database.models.utils import ModelTemplate
from app.database.models.work import WorkModel
from app.database.models.review import ReviewModel


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
    identification_number = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)

    events = relationship("EventModel", back_populates="creator")
    inscriptions = relationship(
        "InscriptionModel",
        back_populates="inscriptor"
    )
    organizers = relationship(
        "OrganizerModel",
        back_populates="organizer"
    )
    chairs = relationship(
        "ChairModel",
        back_populates="chair"
    )
    works_as_author = relationship(
        WorkModel,
        foreign_keys=WorkModel.author_id,
        back_populates="author"
    )
    reviews = relationship(
        ReviewModel,
        foreign_keys=ReviewModel.reviewer_id,
        back_populates="reviewer"
    )
