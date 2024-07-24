from fastapi import APIRouter
from app.submissions.schemas.submission import Submission, SubmissionWithId

submissions_router = APIRouter(
    prefix="/events/{event_id}/works/submissions",
    tags=["Works Submissions"]
)


@submissions_router.put("/latest", status_code=204)
async def update_latest_submission(submission: Submission):
    """
    Updates the work with work_id. The update is always made to
    the latest version of the work: the latest submission.
    If the work stage changes, it creates a new submission.
    """
    pass


@submissions_router.get("/{submission_id}")
async def get_submission(submission_id: int) -> SubmissionWithId:
    """
    Get the submission with submission_id.
    """
    pass
