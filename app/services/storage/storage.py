import os
import json
from google.cloud import storage
from app.schemas.storage.schemas import DownloadURLSchema, UploadURLSchema
from google.oauth2 import service_account
from app.settings.settings import StorageSettings

json_file_content_string = os.getenv('GCP_CREDENTIALS')

if json_file_content_string is None:
    storage_client = None
else:
    try:
        service_account_info = json.loads(json_file_content_string)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info
        )
        storage_client = storage.Client(credentials=credentials)
    except Exception as e:
        print(f"Error initializing storage client: {e}")
        storage_client = None


def generate_signed_upload_url(
    bucket_name,
    blob_name,
    expiration=3600,
    max_size_mb=3
) -> UploadURLSchema:
    blob = __get_blob(bucket_name, blob_name)
    url = blob.generate_signed_url(
        version="v4",
        expiration=expiration,
        method="PUT"
    )

    return UploadURLSchema(
        upload_url=url,
        expiration_time_seconds=expiration,
        max_upload_size_mb=max_size_mb
    )


def generate_signed_read_url(
    bucket_name,
    blob_name,
    expiration=3600,
) -> DownloadURLSchema:
    blob = __get_blob(bucket_name, blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=expiration,
        method="GET"
    )
    return DownloadURLSchema(
        download_url=url,
        expiration_time_seconds=expiration,
    )


def __get_blob(bucket_name, blob_name):
    if not storage_client:
        raise Exception('No Storage Client provided.')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob
