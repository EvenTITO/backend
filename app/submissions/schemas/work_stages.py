from enum import Enum
from typing import Literal, Union
from app.submissions.schemas.work_review import PublicReview, ReviewDecision
from pydantic import BaseModel
from datetime import datetime


class NoReviewStages(str, Enum):
    NO_DECISION = 'NO_DECISION'
    BEFORE_DEADLINE = 'BEFORE_DEADLINE'


class WorkStage(BaseModel):
    stage: Union[ReviewDecision, NoReviewStages]


class MustSubmit(BaseModel):
    deadline_date: datetime


class NumberSubmissions(BaseModel):
    number_submissions: int


class LatestReview(BaseModel):
    latest_review: PublicReview


class BeforeDeadline(WorkStage, MustSubmit):
    stage: Literal[
        NoReviewStages.BEFORE_DEADLINE
    ] = NoReviewStages.BEFORE_DEADLINE


class WaitingDecision(WorkStage, NumberSubmissions):
    stage: Literal[NoReviewStages.NO_DECISION] = NoReviewStages.NO_DECISION


class DeterminedDecision(WorkStage, NumberSubmissions):
    stage: Literal[ReviewDecision.ACCEPTED, ReviewDecision.REJECTED]


class ReSubmitDecision(WorkStage, MustSubmit, NumberSubmissions):
    stage: Literal[ReviewDecision.RESUBMIT] = ReviewDecision.RESUBMIT
    deadline_date: datetime
