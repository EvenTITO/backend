from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.schemas.users.utils import UID


class ReviewAssignment(BaseModel):
    reviewer_id: UID
    work_id: UUID


class PublishReviews(BaseModel):
    work_ids: list[UUID]
    resubmission_deadline: datetime
