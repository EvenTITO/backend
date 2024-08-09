from app.services.storage.storage_service import StorageService
from app.settings.settings import StorageSettings


class WorkStorageService(StorageService):

    async def get_submission_upload_url(self, event_id: str, work_id: int, file_to_get: str):
        storage_settings = StorageSettings()
        return await self.storage_client.generate_signed_upload_url(
            bucket_name=storage_settings.WORKS_BUCKET,
            blob_name=f"{event_id}/works/{work_id}/submissions/{file_to_get}",
        )

    async def get_review_upload_url(self, event_id: str, work_id: int, file_to_get: str):
        storage_settings = StorageSettings()
        return await self.storage_client.generate_signed_upload_url(
            bucket_name=storage_settings.WORKS_BUCKET,
            blob_name=f"{event_id}/works/{work_id}/reviews/{file_to_get}",
        )
