from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.database.models.work import WorkStates
from app.schemas.storage.schemas import UploadURLSchema, DownloadURLSchema


class SubmissionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    work_id: UUID
    event_id: UUID
    state: WorkStates


class SubmissionDownloadSchema(SubmissionResponseSchema):
    model_config = ConfigDict(from_attributes=True)
    download_url: DownloadURLSchema


class SubmissionUploadSchema(SubmissionResponseSchema):
    model_config = ConfigDict(from_attributes=True)
    upload_url: UploadURLSchema
