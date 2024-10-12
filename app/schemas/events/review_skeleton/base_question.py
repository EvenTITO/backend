from pydantic import BaseModel


class BaseQuestion(BaseModel):
    is_mandatory: bool = False
    is_public: bool = False
