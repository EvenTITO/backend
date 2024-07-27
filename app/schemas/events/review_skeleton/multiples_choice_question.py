from pydantic import BaseModel, Field


from typing import Literal


class MultipleChoiceQuestion(BaseModel):
    type_question: Literal['multiple_choice']
    question: str
    options: list[str] = Field(examples=[
        ['first answer', 'second answer', 'third answer']
    ], min_length=2, max_length=20)
    more_than_one_answer_allowed: bool = False
