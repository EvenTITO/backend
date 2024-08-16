from app.schemas.storage.schemas import UploadURLSchema
from app.services.storage.storage_service import StorageService


class WorkStorageService(StorageService):

    async def get_submission_upload_url(self, event_id: str, work_id: int, submission_id: int) -> UploadURLSchema:
        return await self.storage_client.generate_signed_upload_url(
            bucket_name=self.storage_settings.WORKS_BUCKET,
            blob_name=f"{event_id}/works/{work_id}/submissions/{submission_id}",
        )

    async def get_submission_read_url(self, event_id: str, work_id: int, submission_id: int) -> UploadURLSchema:
        return await self.storage_client.generate_signed_read_url(
            bucket_name=self.storage_settings.WORKS_BUCKET,
            blob_name=f"{event_id}/works/{work_id}/submissions/{submission_id}",
        )

    async def get_review_upload_url(self, event_id: str, work_id: int, review_id: str) -> UploadURLSchema:
        return await self.storage_client.generate_signed_upload_url(
            bucket_name=self.storage_settings.WORKS_BUCKET,
            blob_name=f"{event_id}/works/{work_id}/reviews/{review_id}",
        )

    async def get_review_read_url(self, event_id: str, work_id: int, review_id: int) -> UploadURLSchema:
        return await self.storage_client.generate_signed_read_url(
            bucket_name=self.storage_settings.WORKS_BUCKET,
            blob_name=f"{event_id}/works/{work_id}/reviews/{review_id}",
        )
