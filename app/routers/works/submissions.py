from fastapi import APIRouter
from fastapi import Depends
from app.authorization.user_id_dep import verify_user_exists
from app.schemas.works.submission import SubmissionSchema
from app.services.submissions.author_submissions_service_dep import AuthorSubmissionsServiceDep

submissions_router = APIRouter(prefix="/{work_id}/submissions", tags=["Event: Works Submissions"])


@submissions_router.put("/submit", status_code=200, dependencies=[Depends(verify_user_exists)])
async def submit(submission_service: AuthorSubmissionsServiceDep) -> SubmissionSchema:
    return await submission_service.do_submit()
