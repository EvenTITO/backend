from app.schemas.storage.schemas import DownloadURLSchema, UploadURLSchema
from .works import submissions_router


@submissions_router.get("/latest/upload_url")
async def get_upload_submission_file_url() -> UploadURLSchema:
    """
    Obtain the upload URL to update the current submission.
    """
    pass


@submissions_router.get("/{submission_id}/download_url")
async def get_download_submission_file_url(
    submission_id: int
) -> DownloadURLSchema:
    """
    Obtain the download URL to get the signed url for the submission
    with id submission_id.
    """
    pass


@submissions_router.get("/latest/reviews/upload_url")
async def get_upload_review_file_url() -> UploadURLSchema:
    """
    Obtain the upload URL to update the current review for the reviewer.
    The review owner is the reviewer. No one else can edit this review.
    If there is more than one reviewer, each reviewer updates a different file.
    """
    pass


@submissions_router.get("/{submission_id}/reviews/{review_id}/download_url")
async def get_download_review_file_url(
    submission_id: int, review_id: int
) -> DownloadURLSchema:
    """
    Obtain the download URL to get the signed url for the review
    with id (submission_id, review_id).
    """
    pass
