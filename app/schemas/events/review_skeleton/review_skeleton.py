from app.schemas.events.review_skeleton.rating_question import RatingQuestion
from app.schemas.events.review_skeleton.simple_question import SimpleQuestion
from app.schemas.events.review_skeleton.multiples_choice_question import MultipleChoiceQuestion
from typing import Union

from pydantic import BaseModel, Field


class ReviewSkeletonQuestions(BaseModel):
    questions: list[Union[MultipleChoiceQuestion, SimpleQuestion, RatingQuestion]] = Field(default_factory=list)


class ReviewSkeletonSchema(BaseModel):
    review_skeleton: ReviewSkeletonQuestions = Field(default=ReviewSkeletonQuestions())
