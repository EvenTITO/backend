from enum import Enum
from pydantic_settings import BaseSettings


class StorageTypes(str, Enum):
    GCP_STORAGE = "GCP_STORAGE"
    NO_STORAGE = "NO_STORAGE"


class StorageSettings(BaseSettings):
    EVENTS_BUCKET: str
    PUBLIC_BASE_URL: str
    TYPE_STORAGE: StorageTypes
    GCP_CREDENTIALS: str | None
