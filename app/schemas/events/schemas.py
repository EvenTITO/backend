from enum import Enum
from pydantic import (
    BaseModel,
    Field,
)

from ...database.models.event import EventType
from app.schemas.events.dates import DatesCompleteSchema
from app.schemas.events.pricing import PricingSchema


class EventRol(str, Enum):
    ORGANIZER = "ORGANIZER"
    SPEAKER = "SPEAKER"
    ATTENDEE = "ATTENDEE"


class StaticEventSchema(BaseModel):
    title: str = Field(min_length=2, max_length=100,
                       examples=["CONGRESO DE QUIMICA"])
    description: str = Field(max_length=1000, examples=["Evento en FIUBA"])
    event_type: EventType = Field(examples=[EventType.CONFERENCE])


class DynamicGeneralEventSchema(DatesCompleteSchema):
    location: str = Field(
        max_length=200,
        examples=["FIUBA, Av. Paseo Colon 850"],
        default=""
    )
    tracks: list[str] = Field(
        max_length=1000,
        examples=[["track1", "track2", "track3"]],
        default_factory=list
    )
    contact: str = Field(
        max_length=100,
        examples=["Pepe"],
        default=''
    )
    organized_by: str = Field(
        max_length=100,
        examples=["Pepe Argento"],
        default=''
    )


class DynamicEventSchema(DynamicGeneralEventSchema, DatesCompleteSchema, PricingSchema):
    pass
