from typing import Union
from pydantic import BaseModel
from app.schemas.works.author import AuthorInformation
from app.schemas.works.work_stages import (
    BeforeDeadline,
    WaitingDecision,
    DeterminedDecision,
    ReSubmitDecision,
    WorkStage
)


class WorkSchema(BaseModel):
    title: str
    track: str
    abstract: str
    keywords: list[str]
    authors: list[AuthorInformation]


class WorkWithState(WorkSchema):
    state: Union[
        BeforeDeadline,
        WaitingDecision,
        DeterminedDecision,
        ReSubmitDecision
    ]


class BasicWorkInfoForAuthor(WorkSchema, WorkStage):
    id: str


class BasicWorkInfo(BasicWorkInfoForAuthor):
    main_author_name: str
    reviewer_name: str | None = None
