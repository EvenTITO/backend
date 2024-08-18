from pydantic import BaseModel, ConfigDict

from app.schemas.storage.schemas import UploadURLSchema, DownloadURLSchema


class SubmissionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    work_id: str
    event_id: str


class SubmissionDownloadSchema(SubmissionResponseSchema):
    model_config = ConfigDict(from_attributes=True)
    download_url: DownloadURLSchema


class SubmissionUploadSchema(SubmissionResponseSchema):
    model_config = ConfigDict(from_attributes=True)
    upload_url: UploadURLSchema
