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
from ..models.event import EventType, EventStatus
from typing_extensions import Self
from app.storage.events_storage import EventsStaticFiles, get_public_event_url


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


class FeeSchema(BaseModel):
    name: str = Field(examples=['Students Only Fee']),
    description: str = Field(examples=['Only Students with certificate']),
    value: int = Field(examples=[50]),
    currency: str = Field(examples=['ARS'], default='ARS')
    need_verification: bool = Field(
        description='If it is set to True,'
        ' a validation file must be added in the inscription form'
    )


class PricingRateSchema(BaseModel):
    rates: list[FeeSchema]


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


class EventRol(str, Enum):
    ORGANIZER = "ORGANIZER"
    INSCRIPTED = "INSCRIPTED"


class StaticEventSchema(BaseModel):
    title: str = Field(min_length=2, max_length=100,
                       examples=["CONGRESO DE QUIMICA"])
    description: str = Field(max_length=1000, examples=["Evento en FIUBA"])
    event_type: EventType = Field(examples=[EventType.CONFERENCE])


class DynamicEventSchema(BaseModel):
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
    contact: str | None = Field(
        max_length=100,
        examples=["Pepe"],
        default=None
    )
    organized_by: str | None = Field(
        max_length=100,
        examples=["Pepe Argento"],
        default=None
    )
    dates: DatesCompleteSchema | None = None  # TODO: AGREGAR DEFAULT EN VEZ DE NONE.
    pricing: PricingRateSchema | None = None

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


class EventSchema(StaticEventSchema, DynamicEventSchema):
    pass


class EventStatusSchema(BaseModel):
    status: EventStatus = Field(examples=[EventStatus.WAITING_APPROVAL])


class ImgSchema(BaseModel):
    name: str = Field(max_length=100, examples=["main_image_url"])
    url: str = Field(max_length=1000, examples=["https://go.com/img.png"])


class EventSchemaWithEventId(EventSchema, EventStatusSchema):
    id: str = Field(examples=["..."])

    @computed_field
    def media(self) -> list[ImgSchema]:
        return [
            ImgSchema(
                name='main_image_url',
                url=get_public_event_url(self.id, EventsStaticFiles.MAIN_IMAGE)
            ),
            ImgSchema(
                name='brochure_url',
                url=get_public_event_url(self.id, EventsStaticFiles.BROCHURE)
            ),
            ImgSchema(
                name='banner_image_url',
                url=get_public_event_url(
                    self.id, EventsStaticFiles.BANNER_IMAGE),
            )
        ]


class EventModelWithRol(EventSchemaWithEventId):
    model_config = ConfigDict(from_attributes=True)
    roles: list[str] = Field(examples=[["ORGANIZER"]],
                             default=[])


class GeneralEventSchema(DynamicEventSchema):
    notification_mails: list[str] = Field(default_factory=list)


class FullEventSchema(GeneralEventSchema, StaticEventSchema):
    review_skeleton: ReviewSkeletonSchema | None
