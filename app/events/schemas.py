from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from .model import EventType
from typing_extensions import Self


class EventSchema(BaseModel):
    title: str = Field(min_length=2, max_length=100,
                       examples=["CONGRESO DE QUIMICA"])
    start_date: datetime = Field(examples=[datetime(2024, 8, 1)])
    end_date: datetime = Field(examples=[datetime(2024, 8, 2)])
    description: str = Field(max_length=1000, examples=["Evento en FIUBA"])
    event_type: EventType = Field(examples=[EventType.CONFERENCE])

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        start_date = self.start_date
        end_date = self.end_date
        if start_date < datetime.now() or end_date < start_date:
            raise ValueError('Invalid Dates.')
        return self


class ModifyEventSchema(EventSchema):
    id_modifier: str
    id: str


class EventSchemaWithEventId(EventSchema):
    id: str = Field(examples=["..."])
