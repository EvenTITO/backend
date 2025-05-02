import json
from typing import Optional

from google.cloud import storage
from google.oauth2 import service_account

from app.schemas.storage.schemas import DownloadURLSchema, UploadURLSchema
from app.settings.settings import StorageSettings


class GCPStorageClient:
    def __init__(self, gcp_client: storage.Client, settings: StorageSettings):
        self.gcp_client = gcp_client
        self.settings = settings
        self.is_emulator = bool(settings.GCP_EMULATOR_HOST)

    async def generate_signed_upload_url(
        self, bucket_name: str, blob_name: str, expiration: int = 3600, max_size_mb: int = 3
    ) -> UploadURLSchema:
        blob = await self.__get_blob(bucket_name, blob_name)
        url = blob.generate_signed_url(version="v4", expiration=expiration, method="PUT")
        url = self.__maybe_replace_host(url)
        return UploadURLSchema(upload_url=url, expiration_time_seconds=expiration, max_upload_size_mb=max_size_mb)

    async def generate_signed_read_url(
        self,
        bucket_name: str,
        blob_name: str,
        expiration: int = 3600,
    ) -> DownloadURLSchema:
        blob = await self.__get_blob(bucket_name, blob_name)
        url = blob.generate_signed_url(version="v4", expiration=expiration, method="GET")
        url = self.__maybe_replace_host(url)
        return DownloadURLSchema(
            download_url=url,
            expiration_time_seconds=expiration,
        )

    def __maybe_replace_host(self, url: str) -> str:
        if self.is_emulator and self.settings.GCP_EMULATOR_PUBLIC_HOST:
            return url.replace("https://storage.googleapis.com", self.settings.GCP_EMULATOR_PUBLIC_HOST)
        return url

    async def __get_blob(self, bucket_name: str, blob_name: str):
        if not self.gcp_client:
            raise Exception("No Storage Client provided.")
        bucket = self.gcp_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        return blob


def get_gcp_storage_client(storage_settings: StorageSettings) -> GCPStorageClient:
    if storage_settings.GCP_EMULATOR_HOST:
        storage_client = storage.Client(
            project="dummy-project", client_options={"api_endpoint": storage_settings.GCP_EMULATOR_HOST}
        )
    else:
        if storage_settings.GCP_CREDENTIALS is None:
            raise Exception("GCP_CREDENTIALS variable should be set for TYPE_STORAGE=GCP_STORAGE.")
        service_account_info = json.loads(storage_settings.GCP_CREDENTIALS)
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        storage_client = storage.Client(credentials=credentials)

    return GCPStorageClient(storage_client, storage_settings)
