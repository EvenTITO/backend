from pydantic import BaseModel
from datetime import datetime


class ReviewAssignment(BaseModel):
    reviewer_id: str
    work_id: str


class PublishReviews(BaseModel):
    work_ids: list[str]
    resubmission_deadline: datetime
