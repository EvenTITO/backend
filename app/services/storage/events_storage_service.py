
from enum import Enum
from app.schemas.media.image import ImgSchema
from app.services.storage.storage_service import StorageService
from app.settings.settings import StorageSettings


class EventsStaticFiles(str, Enum):
    MAIN_IMAGE = "main_image"
    BANNER_IMAGE = "banner_image"
    BROCHURE = "brochure"


class EventsStorageService(StorageService):
    async def get_public_event_url(self, event_id: str, file_to_get: EventsStaticFiles):
        storage_settings = StorageSettings()
        return await self.get_public_url(
            bucket=storage_settings.EVENTS_BUCKET,
            blob=f"{event_id}/{file_to_get.value}"
        )

    async def get_upload_url(self, event_id: str, file_to_get: EventsStaticFiles):
        storage_settings = StorageSettings()
        return await self.storage_client.generate_signed_upload_url(
            bucket_name=storage_settings.EVENTS_BUCKET,
            blob_name=f"{event_id}/{file_to_get.value}"
        )

    async def get_media(self, event_id: str):
        return [
            ImgSchema(
                name='main_image_url',
                url=await self.get_public_event_url(event_id, EventsStaticFiles.MAIN_IMAGE)
            ),
            ImgSchema(
                name='brochure_url',
                url=await self.get_public_event_url(event_id, EventsStaticFiles.BROCHURE)
            ),
            ImgSchema(
                name='banner_image_url',
                url=await self.get_public_event_url(event_id, EventsStaticFiles.BANNER_IMAGE),
            )
        ]
