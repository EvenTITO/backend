from typing import List

from fastapi import APIRouter, Depends, Query

from app.authorization.author_dep import IsAuthorDep
from app.authorization.chair_dep import IsTrackChairDep
from app.authorization.organizer_dep import IsOrganizerDep
from app.authorization.user_id_dep import verify_user_exists
from app.authorization.util_dep import or_
from app.schemas.works.work import WorkSchema, WorkWithState
from app.services.works.works_service_dep import WorksServiceDep

works_router = APIRouter(prefix="/{event_id}/works", tags=["Events: Works"])


@works_router.get(
    path="",
    status_code=200,
    response_model=List[WorkWithState],
    dependencies=[or_(IsOrganizerDep, IsTrackChairDep)]
)
async def get_works(
        work_service: WorksServiceDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
        track: str | None = Query(default=None)
) -> list[WorkWithState]:
    return await work_service.get_works(track, offset, limit)


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
    dependencies=[or_(IsOrganizerDep, IsAuthorDep, IsTrackChairDep)]
)
#  TODO si sos reviewer de este trabajo tendrias que poder verlo,
async def get_work(work_id: str, work_service: WorksServiceDep) -> WorkWithState:
    return await work_service.get_work(work_id)


@works_router.post(path="", status_code=201, dependencies=[Depends(verify_user_exists)])
async def create_work(work: WorkSchema, work_service: WorksServiceDep) -> int:
    return await work_service.create_work(work)


@works_router.put(path="/{work_id}", status_code=204, dependencies=[Depends(verify_user_exists)])
async def update_work(work_id: str, work_update: WorkSchema, work_service: WorksServiceDep) -> None:
    await work_service.update_work(work_id, work_update)
