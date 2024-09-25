from typing import Literal
from pydantic import BaseModel


class RatingQuestion(BaseModel):
    type_question: Literal['rating']
    question: str
    max_value: int


class RatingAnswer(RatingQuestion):
    answer: int
