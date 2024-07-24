from typing import Union
from pydantic import BaseModel
from app.submissions.schemas.work_stages import (
    BeforeDeadline,
    NumberSubmissions,
    WaitingDecision,
    DeterminedDecision,
    ReSubmitDecision,
    WorkStage
)
from .submission import Submission


class StaticWorkInfo(BaseModel):
    title: str
    track: str


class Work(StaticWorkInfo, Submission):
    pass


class WorkWithState(Work):
    state: Union[
        BeforeDeadline,
        WaitingDecision,
        DeterminedDecision,
        ReSubmitDecision
    ]


class BasicWorkInfo(StaticWorkInfo, WorkStage, NumberSubmissions):
    main_author_name: str
    id: str
    reviewer_name: str | None = None
