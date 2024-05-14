from typing import Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from app.models.event import EventType
from app.utils.exceptions import DatesException


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


class CreateEventSchema(EventSchema):
    id_creator: str


class ModifyEventSchema(EventSchema):
    id_modifier: str
    id: str


class ReplyEventSchema(CreateEventSchema):
    id: str
