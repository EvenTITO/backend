from typing import Union
from pydantic import BaseModel
from app.submissions.schemas.work_stages import (
    BeforeDeadline,
    WaitingDecision,
    DeterminedDecision,
    ReSubmitDecision,
    WorkStage
)
from .submission import Submission


class StaticWorkInfo(BaseModel):
    title: str
    track: str


class WorkSchema(StaticWorkInfo, Submission):
    pass


class WorkWithState(WorkSchema):
    state: Union[
        BeforeDeadline,
        WaitingDecision,
        DeterminedDecision,
        ReSubmitDecision
    ]


class BasicWorkInfoForAuthor(StaticWorkInfo, WorkStage):
    id: str


class BasicWorkInfo(BasicWorkInfoForAuthor):
    main_author_name: str
    reviewer_name: str | None = None
