from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime
from .model import EventType


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


class EventSchemaWithEventId(EventSchema):
    id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "...",
                    "title": "CONGRESO DE QUIMICA",
                    "start_date": datetime(2024, 8, 1),
                    "end_date": datetime(2024, 8, 3),
                    "description": "Evento en FIUBA",
                    "event_type": EventType.CONFERENCE,
                }
            ]
        }
    }


class PublicEventsSchema(BaseModel):
    events: List[dict]

    model_config = ConfigDict(from_attributes=True)
