
from enum import Enum
from app.services.storage.storage import get_public_url, generate_signed_upload_url
from app.settings.settings import StorageSettings


class EventsStaticFiles(str, Enum):
    MAIN_IMAGE = "main_image"
    BANNER_IMAGE = "banner_image"
    BROCHURE = "brochure"


def get_public_event_url(event_id: str, file_to_get: EventsStaticFiles):
    storage_settings = StorageSettings()
    return get_public_url(
        bucket=storage_settings.EVENTS_BUCKET,
        blob=f"{event_id}/{file_to_get.value}"
    )

def get_upload_url(event_id: str, file_to_get: EventsStaticFiles):
    storage_settings = StorageSettings()
    return generate_signed_upload_url(
        bucket_name=storage_settings.EVENTS_BUCKET,
        blob_name=f"{event_id}/{file_to_get.value}"
    )
