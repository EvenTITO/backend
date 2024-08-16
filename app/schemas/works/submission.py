from pydantic import BaseModel, ConfigDict

from app.schemas.storage.schemas import UploadURLSchema


class SubmissionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    upload_url: UploadURLSchema
