from enum import Enum
from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.events.review_skeleton.multiples_choice_question import MultipleChoiceAnswer
from app.schemas.events.review_skeleton.simple_question import SimpleAnswer
from app.schemas.storage.schemas import DownloadURLSchema, UploadURLSchema
from app.schemas.users.utils import UID


class ReviewDecision(str, Enum):
    APPROVED = "APPROVED"
    NOT_APPROVED = "NOT_APPROVED"


class ReviewAnswer(BaseModel):
    answers: list[Union[MultipleChoiceAnswer, SimpleAnswer]] = Field(default_factory=list)


class ReviewCreateRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: ReviewDecision = Field(examples=["APPROVED"])
    review: ReviewAnswer


class ReviewResponseSchema(ReviewCreateRequestSchema):
    id: UUID = Field(examples=["review_id_01"])
    event_id: UUID = Field(examples=["event_id_01"])
    work_id: UUID = Field(examples=["work_id_01"])
    submission_id: UUID = Field(examples=["submission_id_01"])
    reviewer_id: UID = Field(examples=["user_id_01"])


class ReviewDownloadSchema(ReviewResponseSchema):
    model_config = ConfigDict(from_attributes=True)
    download_url: DownloadURLSchema


class ReviewUploadSchema(ReviewResponseSchema):
    model_config = ConfigDict(from_attributes=True)
    upload_url: UploadURLSchema
