from fastapi import APIRouter
from app.submissions.schemas.work import Work, WorkWithState, BasicWorkInfo

works_router = APIRouter(prefix="/events/{event_id}/works", tags=["Works"])


@works_router.post("", status_code=201)
async def create_work(work: Work) -> str:
    """
    Creates the Work. This call is made by the work author.
    """
    pass


@works_router.put("/{work_id}", status_code=204)
async def update_work(work_update: Work):
    """
    Author updates the work with work_id. This method is used only
    in the first stage before the first submission deadline date.
    """
    pass


@works_router.get("/{work_id}/")
async def get_work_author_information() -> WorkWithState:
    """
    Obtain all the work information that the author is allowed
    to see.
    This method is used by the work author.
    """
    pass


@works_router.get("/")
async def get_all_works_basic_information() -> list[BasicWorkInfo]:
    """
    Obtain a resumee of all the works in the event.
    This method is used by the event organizer.
    """
    pass
