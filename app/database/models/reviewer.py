from sqlalchemy import Column, ForeignKey, String

from app.database.models.base import Base
from app.database.models.member import MemberModel


class ReviewerModel(MemberModel, Base):
    __tablename__ = "reviewers"
    work_id = Column(String, ForeignKey("works.id"), primary_key=True)
    # work_ids = Column(ARRAY(String), nullable=True)
