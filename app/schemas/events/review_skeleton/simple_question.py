from pydantic import BaseModel


from typing import Literal


class SimpleQuestion(BaseModel):
    type_question: Literal['simple_question']
    question: str
