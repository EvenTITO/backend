from enum import Enum
from pydantic import BaseModel, Field


# usuario sube un TRABAJO.
# Para subir el TRABAJO debe ser antes del submission_date.

# Antes del SUBMISSION DATE, puede modificar su TRABAJO.

# Desde el SUBMISSION DATE, SOLO puede modificar si esta HABILITADO para modificar.

#


class AuthorInformation(BaseModel):
    full_name: str = Field(examples=['Juan Sanchez'])
    membership: str = Field(examples=['FIUBA'])
    mail: str = Field(examples=['juansanchez@mail.com'])


class Submission(BaseModel):
    title: str
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
    track: str


class SubmissionDecission(Enum, str):
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'
    NO_DECISION = 'NO DECISION'


class SubmissionWithDecision(Submission):
    scores: list[int] = Field(
        description='The scores that were given by the reviewers'
    )
    decision: SubmissionDecission
