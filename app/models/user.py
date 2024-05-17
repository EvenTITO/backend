from sqlalchemy import Column, String
from app.database.database import Base
from sqlalchemy.orm import relationship
from .models_utils import ModelTemplate


class UserModel(ModelTemplate, Base):
    __tablename__ = "users"

    # id = Column(String, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    events = relationship("EventModel", back_populates="creator")
    suscriptions = relationship(
        "SuscriptionModel", back_populates="suscriptor")

    def __repr__(self):
        return f"User({self.id})"
