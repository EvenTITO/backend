from enum import Enum
from app.submissions.schemas.work import Work
from pydantic import BaseModel


class ReviewDecision(str, Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    RESUBMIT = 'RESUBMIT'


class PublicReview(BaseModel):
    review_decision: ReviewDecision
    review_comment: str
