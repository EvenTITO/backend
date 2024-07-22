from __future__ import annotations

from enum import Enum
from typing import Literal, Union
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
    computed_field
)
from datetime import datetime
from .model import EventType, EventStatus
from typing_extensions import Self
from ..organizers.model import InvitationStatus
from app.storage.events_storage import EventsStaticFiles, get_public_event_url


class EventRol(str, Enum):
    ORGANIZER = "ORGANIZER"
    INSCRIPTED = "INSCRIPTED"


class BasicEventSchema(BaseModel):
    title: str = Field(min_length=2, max_length=100,
                       examples=["Congreso de Quimica"], default=None)


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
    tracks: list[str] | None = Field(max_length=1000,
                                     examples=[["track1", "track2", "track3"]],
                                     default=None)
    notification_mails: list[str] | None = Field(examples=[["foo@gmail.com",
                                                            "bar@gmail.com"]],
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


class EventSchemaWithStatusAndId(EventSchema):
    id: str = Field(examples=["..."])
    status: EventStatus = Field(examples=[EventStatus.WAITING_APPROVAL])


class EventSchemaWithEventId(EventSchema):
    id: str = Field(examples=["..."])
    status: EventStatus = Field(examples=[EventStatus.WAITING_APPROVAL])

    @computed_field
    def main_image_url(self) -> str:
        return get_public_event_url(self.id, EventsStaticFiles.MAIN_IMAGE)

    @computed_field
    def banner_image_url(self) -> str:
        return get_public_event_url(self.id, EventsStaticFiles.BANNER_IMAGE)

    @computed_field
    def brochure_url(self) -> str:
        return get_public_event_url(self.id, EventsStaticFiles.BROCHURE)


class EventModelWithRol(EventSchemaWithEventId):
    model_config = ConfigDict(from_attributes=True)
    roles: list[str] = Field(examples=[["ORGANIZER", "SUBSCRIBER"]],
                             default=[])


class CompleteEventSchema(EventModelWithRol):
    review_skeleton: dict | None


class ImgSchema(BaseModel):
    name: str = Field(max_length=100, examples=["main_image_url"])
    url: str = Field(max_length=1000, examples=["https://go.com/img.png"])


class GeneralEventSchema(EventSchemaWithStatusAndId):

    model_config = ConfigDict(from_attributes=True)
    roles: list[str] = Field(examples=[["ORGANIZER", "SUBSCRIBER"]],
                             default=[])

    contact: str | None = Field(max_length=100, examples=["Pepe"])
    organized_by: str | None = Field(max_length=100, examples=["Pepe Argento"])
    review_skeleton: dict | None
    media: list[ImgSchema] | None


class GeneralEventSchemaUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=100,
                       examples=["Congreso de Quimica"], default=None)

    location: str | None = Field(max_length=200,
                                 examples=["FIUBA, Av. Paseo Colon 850"],
                                 default=None)
    contact: str | None = Field(max_length=100,
                                examples=["Pepe"], default=None)
    organized_by: str | None = Field(max_length=100,
                                     examples=["Pepe Argento"], default=None)
    review_skeleton: dict | None = Field(examples=['{"foo":"bar"}'],
                                         default=None)
    tracks: list[str] | None = Field(max_length=1000,
                                     examples=[["track1", "track2", "track3"]],
                                     default=None)
    media: list[ImgSchema] | None = Field(default=None)


# class DatesSchema(BaseModel):
#     dates: dict

class CustomDateSchema(BaseModel):
    name: str = Field(min_length=2, max_length=100,
                      examples=["Presentacion trabajos"], default=None)
    description: str = Field(min_length=2, max_length=100,
                             examples=["Inicio fecha"],
                             default=None)
    value: str = Field(examples=["2023-07-20T15:30:00"], default=None)


class DatesCompleteSchema(BaseModel):
    start_date: str | None = Field(examples=["2023-07-20T15:30:00"],
                                   default=None)
    end_date: str | None = Field(examples=["2023-07-20T15:30:00"],
                                 default=None)
    deadline_submission_date: str | None = Field(
        examples=["2023-07-20T15:30:00"], default=None)
    custom_dates: list[CustomDateSchema]


class DateSchema(BaseModel):
    dates: DatesCompleteSchema


class PricingRateSchema(BaseModel):
    rates: list[dict] = Field(examples=[[{"name": "nombre de la tarifa",
                                          "description": "desc de la tarifa",
                                          "value": "50", "currency": "ARS",
                                          "need_verification": "true"}]],
                              default=None)


class PricingSchema(BasicEventSchema):
    pricing: PricingRateSchema


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


class GeneralEventSchemaUpdateAll(BasicEventSchema):
    rates: list[dict] | None = Field(examples=[[{"name": "nom de la tarifa",
                                                 "description": "desc tarifa",
                                                 "value": "50",
                                                 "currency": "ARS",
                                                 "need_verification":
                                                     "true"}]],
                                     default=None),
    dates: DatesCompleteSchema | None = Field(examples=[
        {"start_date": "2023-07-20T15:30:00",
         "end_date": "2023-07-20T15:30:00",
         "deadline_submission_date": "2023-07-20T15:30:00",
         "custom_dates":
             [{"name": "nombre de la fecha", "description": "desc de la fecha",
               "value": "2023-07-20T15:30:00"}]}], default=None)
    review_skeleton: dict | None = Field(examples=['{"foo":"bar"}'],
                                         default=None)


class ConfigurationEventSchema(GeneralEventSchema):
    rates: list[dict] | None = Field(examples=[[{
        "name": "nombre de la tarifa", "description": "desc de la tarifa",
        "value": "50", "currency": "ARS", "need_verification": "true"}]],
        default=None)
    dates: DatesCompleteSchema | None = Field(examples=[{
        "start_date": "2023-07-20T15:30:00", "end_date": "2023-07-20T15:30:00",
        "deadline_submission_date": "2023-07-20T15:30:00", "custom_dates":
            [{"name": "nombre de la fecha", "description": "desc de la fecha",
              "value": "2023-07-20T15:30:00"}]}], default=None)
    review_skeleton: dict | None = Field(examples=[
        '{"foo":"bar"}'], default=None)


class MultipleChoiceQuestion(BaseModel):
    type_question: Literal['multiple_choice']
    question: str
    options: list[str] = Field(examples=[
        ['first answer', 'second answer', 'third answer']
    ], min_length=2, max_length=20)
    more_than_one_answer_allowed: bool = False


class SimpleQuestion(BaseModel):
    type_question: Literal['simple_question']
    question: str


class ReviewSkeletonSchema(BaseModel):
    questions: list[Union[MultipleChoiceQuestion, SimpleQuestion]]
