from pydantic import (
    BaseModel,
    Field,
)
from datetime import datetime


class CustomDateSchema(BaseModel):
    name: str = Field(min_length=2, max_length=100,
                      examples=["Presentacion trabajos"], default=None)
    description: str = Field(min_length=2, max_length=100,
                             examples=["Inicio fecha"],
                             default=None)
    value: datetime = Field(examples=["2023-07-20T15:30:00"], default=None)


class DatesCompleteSchema(BaseModel):
    start_date: datetime | None = Field(examples=["2023-07-20T15:30:00"],
                                        default=None)
    end_date: datetime | None = Field(examples=["2023-07-20T15:30:00"],
                                      default=None)
    deadline_submission_date: datetime | None = Field(
        examples=["2023-07-20T15:30:00"], default=None)
    custom_dates: list[CustomDateSchema]
