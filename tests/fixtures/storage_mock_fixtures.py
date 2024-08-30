import pytest
from app.schemas.storage.schemas import DownloadURLSchema, UploadURLSchema


@pytest.fixture(scope="function")
async def mock_storage(mocker):
    base_path = 'app.services.storage.storage_clients'
    gcp_path = base_path + '.gcp_storage_client.GCPStorageClient'
    no_client_path = base_path + '.no_storage_provided_client.NoStorageProvidedClient'

    def mock_generate_upload_url(method_to_mock):
        mock_value = mocker.patch(method_to_mock)
        mock_value.return_value = UploadURLSchema(
            upload_url='mocked-url-upload',
            expiration_time_seconds=3600,
            max_upload_size_mb=5
        )

    def mock_generate_download_url_mock(method_to_mock):
        mock_value = mocker.patch(method_to_mock)
        mock_value.return_value = DownloadURLSchema(
            download_url='mocked-url-download',
            expiration_time_seconds=3600,
        )

    mock_generate_upload_url(gcp_path+'.generate_signed_upload_url')
    mock_generate_download_url_mock(gcp_path+'.generate_signed_read_url')

    mock_generate_upload_url(no_client_path+'.generate_signed_upload_url')
    mock_generate_download_url_mock(no_client_path+'.generate_signed_read_url')

    yield
