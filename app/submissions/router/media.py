from .works import works_router
from fastapi import Query


@works_router.get("/{work_id}/upload_url")
async def get_upload_file_url():
    """
    Obtain the upload URL to update the current submission.
    """
    pass


@works_router.get("/{work_id}/download_url")
async def get_download_submission_file_url(submission_id: int = Query()):
    """
    Obtain the download URL to get the signed url for the submission
    with id submission_id.
    """
    pass
