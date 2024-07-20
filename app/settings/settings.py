from pydantic_settings import BaseSettings


class StorageSettings(BaseSettings):
    EVENTS_BUCKET: str
    PUBLIC_BASE_URL: str
