from app.storage.schemas import DownloadURLSchema, UploadURLSchema


def mock_storage_functions(mocker):
    generate_upload_url_mock = mocker.patch(
        'app.storage.storage.generate_signed_upload_url'
    )
    generate_upload_url_mock.return_value = UploadURLSchema(
        upload_url='mocked-url-upload',
        expiration_time_seconds=3600,
        max_upload_size_mb=5
    )

    generate_download_url_mock = mocker.patch(
        'app.storage.storage.generate_signed_read_url'
    )
    generate_download_url_mock.return_value = DownloadURLSchema(
        download_url='mocked-url-download',
        expiration_time_seconds=3600,
    )

    return generate_upload_url_mock, generate_download_url_mock
