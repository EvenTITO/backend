from typing import Literal

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self


class MultipleChoiceQuestion(BaseModel):
    type_question: Literal['multiple_choice']
    question: str
    options: list[str] = Field(examples=[
        ['first answer', 'second answer', 'third answer']
    ], min_length=2, max_length=20)
    more_than_one_answer_allowed: bool = False


class MultipleChoiceAnswer(MultipleChoiceQuestion):
    answers: list[str] = Field(examples=[['first answer', 'second answer']])

    @model_validator(mode='after')
    def check_answers(self) -> Self:
        if not self.more_than_one_answer_allowed and len(self.answers) > 1:
            raise ValueError("Only one answer allowed")
        if not all(answer in self.options for answer in self.answers):
            raise ValueError("All answers should be contained in options")
        return self
