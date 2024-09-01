from typing import Literal

from pydantic import BaseModel


class SimpleQuestion(BaseModel):
    type_question: Literal['simple_question']
    question: str


class SimpleAnswer(SimpleQuestion):
    answer: str
