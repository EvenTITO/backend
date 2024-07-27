from app.schemas.events.review_skeleton.simple_question import SimpleQuestion
from app.schemas.events.review_skeleton.multiples_choice_question import MultipleChoiceQuestion
from typing import Union

from pydantic import BaseModel


class ReviewSkeletonSchema(BaseModel):
    questions: list[Union[MultipleChoiceQuestion, SimpleQuestion]]
