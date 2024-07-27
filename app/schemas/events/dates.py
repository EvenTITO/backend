from enum import Enum
import datetime
from pydantic import (
    BaseModel,
    Field,
)
# from datetime import datetime


# class CustomDateSchema(BaseModel):
#     name: str = Field(min_length=2, max_length=100,
#                       examples=["Presentacion trabajos"], default=None)
#     description: str = Field(min_length=2, max_length=100,
#                              examples=["Inicio fecha"],
#                              default=None)
#     value: datetime = Field(examples=["2023-07-20T15:30:00"], default=None)


# class DatesCompleteSchema(BaseModel):
#     start_date: datetime | None = Field(examples=["2023-07-20T15:30:00"],
#                                         default=None)
#     end_date: datetime | None = Field(examples=["2023-07-20T15:30:00"],
#                                       default=None)
#     deadline_submission_date: datetime | None = Field(
#         examples=["2023-07-20T15:30:00"], default=None)
#     custom_dates: list[CustomDateSchema]

class MandatoryDates(str, Enum):
    START_DATE = 'START_DATE'
    END_DATE = 'END_DATE'
    SUBMISSION_DEADLINE_DATE = 'SUBMISSION_DEADLINE_DATE'


class DateSchema(BaseModel):
    name: MandatoryDates | None = Field(
        min_length=2,
        max_length=100,
        examples=[MandatoryDates.START_DATE],
        default=None
    )
    label: str = Field(
        min_length=2,
        max_length=100,
        examples=["Presentacion trabajos"]
    )
    description: str = Field(
        min_length=2,
        max_length=100,
        examples=["Inicio fecha"]
    )
    is_mandatory: bool
    date: datetime.date | None = Field(examples=["2023-07-12"], default=None)
    time: datetime.time | None = Field(examples=["15:30"], default=None)


class DatesCompleteSchema(BaseModel):
    dates: list[DateSchema] = Field(
        default=[
            DateSchema(
                name=MandatoryDates.START_DATE,
                label='Fecha de Comienzo',
                description='Fecha de comienzo del evento.',
                is_mandatory=True
            ),
            DateSchema(
                name=MandatoryDates.END_DATE,
                label='Fecha de Finalización',
                description='Fecha de comienzo del evento.',
                is_mandatory=True
            ),
            DateSchema(
                name=MandatoryDates.SUBMISSION_DEADLINE_DATE,
                label='Fecha de envío de trabajos',
                description='Fecha límite de envío de trabajos.',
                is_mandatory=True
            )
        ]
    )
    # TODO: add validator: all mandatory dates should be present with is_mandatory true.
    # TODO: validate start date before end date.
    # TODO: validate submission date before start date.
    # TODO: solo debe haber 3 mandatory que son esas 3 separadas.

    # @model_validator(mode='after')
    # def check_dates(self) -> Self:
    #     start_date = self.start_date
    #     end_date = self.end_date
    #     if start_date is None and end_date is None:
    #         return self
    #     if start_date is None or end_date is None:
    #         raise ValueError('Both start_date and"\
    #                          " end_date must be specified.')
    #     if start_date < datetime.now() or end_date < start_date:
    #         raise ValueError('Invalid Dates.')
    #     return self
