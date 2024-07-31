class NoStorageProvidedClient:
    async def generate_signed_upload_url(
        self,
        bucket_name,
        blob_name,
        expiration,
        max_size_mb
    ):
        raise Exception("No storage Client provided")

    async def generate_signed_read_url(
        self,
        bucket_name,
        blob_name,
        expiration,
    ):
        raise Exception("No storage Client provided")
