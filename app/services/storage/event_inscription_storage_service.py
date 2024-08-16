from app.services.storage.storage_service import StorageService


class EventInscriptionStorageService(StorageService):

    async def get_affiliation_upload_url(self, event_id: str, user_id: str, inscription_id: int):
        return await self.storage_client.generate_signed_upload_url(
            bucket_name=self.storage_settings.CERTIFICATES_BUCKET,
            blob_name=f"{event_id}/users/{user_id}/affiliations/{inscription_id}",
        )

    async def get_affiliation_read_url(self, event_id: str, user_id: str, inscription_id: int):
        return await self.storage_client.generate_signed_read_url(
            bucket_name=self.storage_settings.CERTIFICATES_BUCKET,
            blob_name=f"{event_id}/users/{user_id}/affiliations/{inscription_id}",
        )

    async def get_payment_upload_url(self, event_id: str, user_id: str, inscription_id: str):
        return await self.storage_client.generate_signed_upload_url(
            bucket_name=self.storage_settings.CERTIFICATES_BUCKET,
            blob_name=f"{event_id}/users/{user_id}/payments/{inscription_id}",
        )

    async def get_payment_read_url(self, event_id: str, user_id: str, inscription_id: str):
        return await self.storage_client.generate_signed_read_url(
            bucket_name=self.storage_settings.CERTIFICATES_BUCKET,
            blob_name=f"{event_id}/users/{user_id}/payments/{inscription_id}",
        )
