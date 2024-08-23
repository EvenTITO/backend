from typing import List

from fastapi import APIRouter, Depends

from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.organizer_or_admin_dep import verify_is_organizer_or_admin
from app.authorization.organizer_or_chair_dep import verify_is_organizer_or_chair
from app.schemas.members.chair_schema import ChairResponseSchema, ChairRequestSchema
from app.services.event_chairs.event_chairs_service_dep import EventChairServiceDep

event_chairs_router = APIRouter(prefix="/{event_id}/chairs", tags=["Events: Chairs"])


@event_chairs_router.get(
    path="",
    response_model=List[ChairResponseSchema],
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def read_event_chairs(chair_service: EventChairServiceDep, event_id: str) -> List[ChairResponseSchema]:
    return await chair_service.get_all_chairs(event_id)


@event_chairs_router.get(
    path="/{user_id}",
    response_model=ChairResponseSchema,
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def get_chair(event_id: str, user_id: str, chair_service: EventChairServiceDep) -> ChairResponseSchema:
    return await chair_service.get_chair(event_id, user_id)


@event_chairs_router.get(
    path="/me",
    response_model=ChairResponseSchema,
    dependencies=[Depends(verify_is_organizer_or_chair)]
)
async def get_my_chair(
        event_id: str,
        caller_id: CallerIdDep,
        chair_service: EventChairServiceDep
) -> ChairResponseSchema:
    return await chair_service.get_chair(event_id, caller_id)


@event_chairs_router.delete(
    path="/{user_id}",
    status_code=201,
    response_model=None,
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def remove_chair(
        event_id: str,
        user_id: str,
        chair_service: EventChairServiceDep
) -> None:
    await chair_service.remove_chair(event_id, user_id)


@event_chairs_router.put(
    path="/{user_id}/tracks",
    status_code=201,
    response_model=None,
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def update(
        tracks: ChairRequestSchema,
        event_id: str,
        user_id: str,
        chair_service: EventChairServiceDep
) -> None:
    await chair_service.update_tracks(event_id, user_id, tracks)
