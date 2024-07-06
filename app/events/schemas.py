from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime
from .model import EventType, EventStatus
from typing_extensions import Self

from ..organizers.model import InvitationStatus


class EventRol(str, Enum):
    ORGANIZER = "ORGANIZER"
    INSCRIPTED = "INSCRIPTED"


class EventSchema(BaseModel):
    title: str = Field(min_length=2, max_length=100,
                       examples=["CONGRESO DE QUIMICA"])
    description: str = Field(max_length=1000, examples=["Evento en FIUBA"])
    event_type: EventType = Field(examples=[EventType.CONFERENCE])
    start_date: datetime | None = Field(examples=[datetime(2024, 8, 1)],
                                        default=None)
    end_date: datetime | None = Field(examples=[datetime(2024, 8, 2)],
                                      default=None)
    location: str | None = Field(max_length=200,
                                 examples=["FIUBA, Av. Paseo Colon 850"],
                                 default=None)
    tracks: str | None = Field(max_length=1000,
                               examples=["track1, track2, track3"],
                               default=None)

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        start_date = self.start_date
        end_date = self.end_date
        if start_date is None and end_date is None:
            return self
        if start_date is None or end_date is None:
            raise ValueError('Both start_date and"\
                             " end_date must be specified.')
        if start_date < datetime.now() or end_date < start_date:
            raise ValueError('Invalid Dates.')
        return self


class ModifyEventStatusSchema(BaseModel):
    status: EventStatus = Field(examples=[EventStatus.WAITING_APPROVAL])


class EventSchemaWithEventId(EventSchema):
    id: str = Field(examples=["..."])
    status: EventStatus = Field(examples=[EventStatus.WAITING_APPROVAL])


# # TODO: implementar!
# class EventProfileWithIdSchema(EventSchema):
#     id: str = Field(examples=["..."])
#     status: EventStatus = Field(examples=[EventStatus.WAITING_APPROVAL])
class EventModelWithRol(EventSchemaWithEventId):
    model_config = ConfigDict(from_attributes=True)
    roles: list[str] = Field(examples=[["ORGANIZER", "SUBSCRIBER"]],
                             default=[])


class CompleteEventSchema(EventModelWithRol):
    review_skeleton: dict | None


class DatesSchema(BaseModel):
    dates: dict


class PricingSchema(BaseModel):
    pricing: dict


class ReviewSkeletonSchema(BaseModel):
    review_skeleton: dict

# title: str = Field(min_length=2, max_length=100,
#                    examples=["CONGRESO DE QUIMICA"])
# description: str = Field(max_length=1000, examples=["Evento en FIUBA"])
# event_type: EventType = Field(examples=[EventType.CONFERENCE])
# start_date: datetime | None = Field(examples=[datetime(2024, 8, 1)],
#                                     default=None)


class ReviewerSchema(BaseModel):
    invitation_expiration_date: datetime | None = \
        Field(examples=[datetime(2024, 12, 9)], default=None)
    invitation_status: str = Field(examples=[InvitationStatus.INVITED])
    tracks: str | None = Field(max_length=1000,
                               examples=["track1, track2, track3"],
                               default=None)

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.invitation_expiration_date <= datetime.now():
            raise ValueError('Invalid invitation expiration date.')
        return self


class ReviewerSchemaComplete(ReviewerSchema):
    id_user: str = Field(examples=["..."])
