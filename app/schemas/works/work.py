from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.database.models.work import WorkStates
from app.schemas.works.author import AuthorInformation


class WorkSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    track: str
    abstract: str
    keywords: list[str]
    authors: list[AuthorInformation]


class WorkStateSchema(BaseModel):
    state: WorkStates


class WorkWithState(WorkSchema, WorkStateSchema):
    id: UUID
    deadline_date: datetime
