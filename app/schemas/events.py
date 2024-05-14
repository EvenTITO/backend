from pydantic import BaseModel, Field
from datetime import datetime
from app.models.event import EventType


class EventSchema(BaseModel):
    title: str = Field(min_length=2)
    start_date: datetime
    end_date: datetime
    description: str
    event_type: EventType

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "CONGRESO DE QUIMICA",
                    "start_date": datetime(2024, 8, 1),
                    "end_date": datetime(2024, 8, 3),
                    "description": "Evento en FIUBA",
                    "event_type": EventType.CONFERENCE,
                }
            ]
        }
    }

    # @validator("end_date")
    # def check_dates(cls, v: str, values: dict[str, Any]) -> str:
    #     start_date = values["start_date"]
    #     end_date = v

    #     if (
    #         (start_date is None and end_date is not None) or
    #         (start_date is not None and end_date is None)
    #     ):
    #         raise ValueError('You must set both dates')
    #     elif end_date < start_date:
    #         raise ValueError('')
    #     else:
    #         return v


class CreateEventSchema(EventSchema):
    id_creator: str


class ModifyEventSchema(EventSchema):
    id_modifier: str
    id: str


class ReplyEventSchema(CreateEventSchema):
    id: str
