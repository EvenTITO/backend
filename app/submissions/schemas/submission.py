from pydantic import BaseModel, Field
from .author import AuthorInformation


class Submission(BaseModel):
    abstract: str
    keywords: list[str]
    authors: list[AuthorInformation]
    notifications_mails: list[str] = Field(
        examples=[
            [
                'juansanchez@mail.com',
                'martinasanchez@mail.com'
            ]
        ]
    )


class SubmissionWithId(Submission):
    id: int
