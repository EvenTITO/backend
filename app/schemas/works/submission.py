from pydantic import BaseModel, ConfigDict


class SubmissionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    upload_url: str
