
from enum import Enum
from .storage import get_public_url
from settings.settings import StorageSettings


class EventsStaticFiles(str, Enum):
    MAIN_IMAGE = "main_image"
    BANNER_IMAGE = "banner_image"
    BROCHURE = "brochure"


def get_public_event_url(file_to_get: EventsStaticFiles):
    storage_settings = StorageSettings()
    return get_public_url(
        bucket=storage_settings.EVENTS_BUCKET,
        blob=file_to_get
    )
