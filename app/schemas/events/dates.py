from enum import Enum
# import datetime
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

# class MandatoryDates(str, Enum):
#     START_DATE = 'START_DATE'
#     END_DATE = 'END_DATE'
#     SUBMISSION_DEADLINE_DATE = 'SUBMISSION_DEADLINE_DATE'


# class DateSchema(BaseModel):
#     name: MandatoryDates | None = Field(
#         min_length=2,
#         max_length=100,
#         examples=[MandatoryDates.START_DATE],
#         default=None
#     )
#     label: str = Field(
#         min_length=2,
#         max_length=100,
#         examples=["Presentacion trabajos"]
#     )
#     description: str = Field(
#         min_length=2,
#         max_length=100,
#         examples=["Inicio fecha"]
#     )
#     is_mandatory: bool
#     date: datetime.date = Field(examples=["2023-07-12"])
#     time: datetime.time = Field(examples=["15:30"])


# class DatesCompleteSchema(BaseModel):
#     dates: list[DateSchema]
