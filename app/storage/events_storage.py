
from enum import Enum
from .storage import get_public_url, StorageClient
from app.settings.settings import StorageSettings


class EventsStaticFiles(str, Enum):
    MAIN_IMAGE = "main_image"
    BANNER_IMAGE = "banner_image"
    BROCHURE = "brochure"


def get_public_event_url(event_id: str, file_to_get: EventsStaticFiles):
    storage_settings = StorageSettings()
    return get_public_url(
        bucket=storage_settings.EVENTS_BUCKET,
        blob=f"{event_id}/{file_to_get}"
    )


def get_upload_url(event_id: str, file_to_get: EventsStaticFiles):
    storage_settings = StorageSettings()
    storage_client = StorageClient()
    return storage_client.generate_signed_upload_url(
        bucket_name=storage_settings.EVENTS_BUCKET,
        blob_name=f"{event_id}/{file_to_get}"
    )
