from pydantic import BaseModel, Field
from .author import AuthorInformation


class Submission(BaseModel):
    abstract: str
    keywords: list[str]
    authors: list[AuthorInformation]


class SubmissionWithId(Submission):
    id: int
