from typing import Annotated
from uuid import UUID

from annotated_types import Len
from pydantic import BaseModel, ConfigDict, Field

from app.database.models.inscription import InscriptionRole, InscriptionStatus
from app.schemas.storage.schemas import UploadURLSchema, DownloadURLSchema
from app.schemas.users.utils import UID


class InscriptionIdSchema(BaseModel):
    id: UUID


class InscriptionDownloadSchema(InscriptionIdSchema):
    model_config = ConfigDict(from_attributes=True)
    download_url: DownloadURLSchema | None = Field(default=None)


class InscriptionUploadSchema(InscriptionIdSchema):
    model_config = ConfigDict(from_attributes=True)
    upload_url: UploadURLSchema | None = Field(default=None)


class InscriptionRequestSchema(BaseModel):
    roles: Annotated[list[InscriptionRole], Len(min_length=1)]
    affiliation: str | None = Field(default=None)


class InscriptionResponseSchema(InscriptionRequestSchema, InscriptionUploadSchema):
    user_id: UID
    event_id: UUID
    status: InscriptionStatus
