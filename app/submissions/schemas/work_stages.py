from typing import Literal
from app.submissions.schemas.work_review import PublicReview, ReviewDecision
from pydantic import BaseModel
from datetime import datetime


class StageEnum(ReviewDecision):
    NO_DECISION = 'NO_DECISION'
    BEFORE_DEADLINE = 'BEFORE_DEADLINE'


class WorkStage(BaseModel):
    stage: StageEnum


class MustSubmit(BaseModel):
    deadline_date: datetime


class NumberSubmissions(BaseModel):
    number_submissions: int


class LatestReview(BaseModel):
    latest_review: PublicReview


class BeforeDeadline(WorkStage, MustSubmit):
    stage: Literal[StageEnum.BEFORE_DEADLINE] = StageEnum.BEFORE_DEADLINE


class WaitingDecision(WorkStage, NumberSubmissions):
    stage: Literal[StageEnum.NO_DECISION] = StageEnum.NO_DECISION


class DeterminedDecision(WorkStage, NumberSubmissions):
    stage: Literal[StageEnum.ACCEPTED, StageEnum.REJECTED]


class ReSubmitDecision(WorkStage, MustSubmit, NumberSubmissions):
    stage: Literal[StageEnum.RESUBMIT] = StageEnum.RESUBMIT
    deadline_date: datetime
