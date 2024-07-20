from pydantic import BaseModel


class UploadURLSchema(BaseModel):
    upload_url: str
    expiration_time_seconds: int
    max_upload_size_mb: int


class DownloadURLSchema(BaseModel):
    download_url: str
    expiration_time_seconds: int
