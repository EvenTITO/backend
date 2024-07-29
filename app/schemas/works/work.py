from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.work import WorkStates
from app.schemas.works.author import AuthorInformation


class WorkSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    track: str
    abstract: str
    keywords: list[str]
    authors: list[AuthorInformation]


class WorkWithState(WorkSchema):
    id: int
    state: WorkStates
    deadline_date: datetime


# class BasicWorkInfo(BasicWorkInfoForAuthor):
#     main_author_name: str
#     reviewer_name: str | None = None
