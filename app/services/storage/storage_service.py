from app.services.services import BaseService
from app.services.storage.storage_clients.gcp_storage_client import get_gcp_storage_client
from app.services.storage.storage_clients.no_storage_provided_client import NoStorageProvidedClient
from app.settings.settings import StorageSettings, StorageTypes

storage_settings = StorageSettings()


def get_storage_client():
    try:
        if storage_settings.TYPE_STORAGE == StorageTypes.GCP_STORAGE:
            return get_gcp_storage_client(storage_settings)
        return NoStorageProvidedClient()
    except Exception as e:
        print(f"Error initializing storage client: {str(e)}")
        return NoStorageProvidedClient()


# this must be called only once to have only one storage client up (not one for each request).
storage_client = get_storage_client()


class StorageService(BaseService):
    def __init__(self):
        self.storage_client = storage_client

    async def get_public_url(self, bucket, blob):
        return StorageSettings().PUBLIC_BASE_URL + bucket + '/' + blob
