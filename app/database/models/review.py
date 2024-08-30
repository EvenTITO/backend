from sqlalchemy import (
    Column,
    ForeignKey,
    JSON,
    UUID, String, Boolean
)

from app.database.models.utils import UIDType, ModelTemplate


class ReviewModel(ModelTemplate):
    __tablename__ = "reviews"

    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id"))
    reviewer_id = Column(UIDType, ForeignKey("users.id"))
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id"))
    status = Column(String)
    review = Column(JSON)
    shared = Column(Boolean, default=False)
