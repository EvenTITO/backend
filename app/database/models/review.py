from sqlalchemy import (
    Column,
    ForeignKey,
    JSON,
    UUID, String, Boolean
)

from app.database.models.base import Base
from app.database.models.utils import UIDType, ModelTemplate
from sqlalchemy.orm import relationship


class ReviewModel(ModelTemplate, Base):
    __tablename__ = "reviews"

    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id"))
    reviewer_id = Column(UIDType, ForeignKey("users.id"))
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id"))
    status = Column(String)
    review = Column(JSON)
    shared = Column(Boolean, default=False)

    # Always fetch the usermodel, when fetching a review
    reviewer = relationship("UserModel", back_populates='reviews', lazy=False)
