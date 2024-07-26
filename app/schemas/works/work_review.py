from enum import Enum
from pydantic import BaseModel


class ReviewDecision(str, Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    RESUBMIT = 'RESUBMIT'


class PublicReview(BaseModel):
    review_decision: ReviewDecision
    review_comment: str
