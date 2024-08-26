from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class ReviewAssignment(BaseModel):
    reviewer_id: str
    work_id: UUID


class PublishReviews(BaseModel):
    work_ids: list[str]
    resubmission_deadline: datetime
