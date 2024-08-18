from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, ConfigDict

from app.database.models.inscription import InscriptionRole, InscriptionStatus
from app.schemas.storage.schemas import UploadURLSchema, DownloadURLSchema


class InscriptionRequestSchema(BaseModel):
    roles: Annotated[list[InscriptionRole], Len(min_length=1)]
    affiliation: str | None


class InscriptionResponseSchema(BaseModel):
    id: str
    user_id: str
    event_id: str
    roles: list[InscriptionRole]
    status: InscriptionStatus
    affiliation: str | None
    affiliation_upload_url: UploadURLSchema | None


class InscriptionPayResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    upload_url: UploadURLSchema


class InscriptionAffiliationUploadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    upload_url: UploadURLSchema


class InscriptionAffiliationDownloadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    download_url: DownloadURLSchema
