from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.member import MemberModel


class ReviewerModel(MemberModel, Base):
    __tablename__ = "reviewers"
    work_id = Column(String, ForeignKey("works.id"), primary_key=True)
    organizer = relationship("UserModel", back_populates="reviewers")
    event = relationship("EventModel", back_populates="reviewers")
    work = relationship("WorkModel", back_populates="reviewers")
