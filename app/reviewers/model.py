from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.utils.models_utils import DateTemplate


class ReviewerModel(DateTemplate, Base):
    __tablename__ = "reviewers"

    id_reviewer = Column(String, ForeignKey("users.id"), primary_key=True)
    id_event = Column(String, ForeignKey("events.id"), primary_key=True)

    reviewer = relationship("UserModel", back_populates="assigned_reviews")
    event = relationship("EventModel", back_populates="reviewers")
