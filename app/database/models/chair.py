from sqlalchemy import Column, String, ARRAY
from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.member import MemberModel


class ChairModel(MemberModel, Base):
    __tablename__ = "chairs"
    tracks = Column(ARRAY(String))
    chair = relationship("UserModel", back_populates="chairs")
    event = relationship("EventModel", back_populates="chairs")
