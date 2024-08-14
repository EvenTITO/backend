from enum import Enum

from app.schemas.media.image import ImgSchema
from app.services.storage.storage_service import StorageService
from app.settings.settings import StorageSettings


class EventsStaticFiles(str, Enum):
    MAIN_IMAGE = "main_image"
    BANNER_IMAGE = "banner_image"
    BROCHURE = "brochure"


class EventsStorageService(StorageService):

    async def get_upload_url(self, event_id: str, file_to_get: EventsStaticFiles):
        return await self.storage_client.generate_signed_upload_url(
            bucket_name=self.storage_settings.EVENTS_BUCKET,
            blob_name=f"{event_id}/{file_to_get.value}"
        )

    @staticmethod
    def get_public_event_url(event_id: str, file_to_get: EventsStaticFiles):
        storage_settings = StorageSettings()
        return storage_settings.PUBLIC_BASE_URL + storage_settings.EVENTS_BUCKET + f"/{event_id}/{file_to_get.value}"

    @staticmethod
    def get_media(event_id: str):
        return [
            ImgSchema(
                name=EventsStaticFiles.MAIN_IMAGE,
                url=EventsStorageService.get_public_event_url(event_id, EventsStaticFiles.MAIN_IMAGE)
            ),
            ImgSchema(
                name=EventsStaticFiles.BROCHURE,
                url=EventsStorageService.get_public_event_url(event_id, EventsStaticFiles.BROCHURE)
            ),
            ImgSchema(
                name=EventsStaticFiles.BANNER_IMAGE,
                url=EventsStorageService.get_public_event_url(event_id, EventsStaticFiles.BANNER_IMAGE)
            )
        ]
