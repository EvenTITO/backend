from fastapi import APIRouter, Query
from fastapi import Depends

from app.authorization.organizer_or_admin_dep import verify_is_organizer
from app.authorization.organizer_or_author_dep import verify_is_organizer_or_author
from app.authorization.user_id_dep import verify_user_exists
from app.schemas.works.submission import SubmissionUploadSchema, SubmissionDownloadSchema, SubmissionResponseSchema
from app.services.submissions.submissions_service_dep import SubmissionsServiceDep

works_submissions_router = APIRouter(
    prefix="/{event_id}/works/{work_id}/submissions",
    tags=["Event: Works Submissions"]
)
submissions_router = APIRouter(prefix="/{event_id}/submissions", tags=["Event: Submissions"])


@works_submissions_router.put(path="/submit", status_code=200, dependencies=[Depends(verify_user_exists)])
async def submit(submission_service: SubmissionsServiceDep) -> SubmissionUploadSchema:
    return await submission_service.do_submit()


@works_submissions_router.get(path="/{submission_id}", status_code=200,
                              dependencies=[Depends(verify_is_organizer_or_author)])
async def get_download_submission_file(
        submission_id: str,
        submission_service: SubmissionsServiceDep
) -> SubmissionDownloadSchema:
    return await submission_service.get_submission(submission_id)


@works_submissions_router.get(path="/latest", status_code=200, dependencies=[Depends(verify_is_organizer_or_author)])
async def get_download_latest_submission_file(
        submission_service: SubmissionsServiceDep) -> SubmissionDownloadSchema:
    return await submission_service.get_latest_submission()


@submissions_router.get(path="", status_code=200, dependencies=[Depends(verify_is_organizer)])
async def get_all_submissions(
        submission_service: SubmissionsServiceDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100)
) -> list[SubmissionResponseSchema]:
    return await submission_service.get_all_event_submissions(offset, limit)
