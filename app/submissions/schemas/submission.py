from pydantic import BaseModel
from .author import AuthorInformation


class Submission(BaseModel):
    abstract: str
    keywords: list[str]
    authors: list[AuthorInformation]


class SubmissionWithId(Submission):
    id: int
