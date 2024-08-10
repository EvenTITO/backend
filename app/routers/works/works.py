from typing import List

from fastapi import APIRouter, Depends, Query

from app.authorization.organizer_or_admin_dep import verify_is_organizer
from app.authorization.user_id_dep import verify_user_exists
from app.routers.works.submissions import submissions_router
from app.schemas.works.work import WorkSchema, WorkWithState
from app.services.works.author_works_service_dep import AuthorWorksServiceDep
from app.services.works.works_service_dep import WorksServiceDep

works_router = APIRouter(prefix="/{event_id}/works", tags=["Events: Works"])
works_router.include_router(submissions_router)


@works_router.get(
    path="/",
    status_code=200,
    response_model=List[WorkWithState],
    dependencies=[Depends(verify_is_organizer)]
)
async def get_all_works(
        work_service: WorksServiceDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100)
) -> list[WorkWithState]:
    return await work_service.get_all_event_works(offset, limit)


@works_router.get(
    path="/my-works",
    status_code=200,
    response_model=List[WorkWithState],
    dependencies=[Depends(verify_user_exists)]
)
async def read_my_works(
        work_service: WorksServiceDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100)
) -> list[WorkWithState]:
    return await work_service.get_my_works(offset, limit)


@works_router.get(
    path="/{work_id}",
    status_code=200,
    response_model=WorkWithState,
    dependencies=[Depends(verify_user_exists)]
)
async def get_work_author_information(work_service: AuthorWorksServiceDep) -> WorkWithState:
    return await work_service.get_work()


@works_router.post(path="", status_code=201, dependencies=[Depends(verify_user_exists)])
async def create_work(work: WorkSchema, work_service: WorksServiceDep) -> int:
    return await work_service.create_work(work)


@works_router.put(path="/{work_id}", status_code=204, dependencies=[Depends(verify_user_exists)])
async def update_work(work_update: WorkSchema, work_service: AuthorWorksServiceDep) -> None:
    await work_service.update_work(work_update)
