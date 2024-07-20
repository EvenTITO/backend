import os
import json
from google.cloud import storage
from google.oauth2 import service_account
from settings.settings import StorageSettings
json_file_content_string = os.getenv('GCP_CREDENTIALS')

service_account_info = json.loads(json_file_content_string)
credentials = service_account.Credentials.from_service_account_info(
    service_account_info
)


def get_public_url(bucket, blob):
    return StorageSettings().PUBLIC_BASE_URL + bucket + '/' + blob


class StorageClient:
    def generate_signed_upload_url(
        self,
        bucket_name,
        blob_name,
        expiration=3600,
        max_size_mb=3
    ):
        blob = self.__get_blob(bucket_name, blob_name)
        url = blob.generate_signed_url(
            version="v4",
            expiration=expiration,
            method="PUT"
        )

        return url

    def generate_signed_read_url(
        self,
        bucket_name,
        blob_name,
        expiration=3600,
    ):
        blob = self.__get_blob(bucket_name, blob_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=expiration,
            method="GET"
        )
        return url

    def __get_blob(self, bucket_name, blob_name):
        self._client = storage.Client(credentials=credentials)
        bucket = self._client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        return blob
