from typing import List

from fastapi import APIRouter, Depends

from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.organizer_or_admin_dep import verify_is_organizer
from app.authorization.user_id_dep import verify_user_exists
from app.schemas.members.chair_schema import ChairRequestSchema, ChairResponseSchema
from app.services.event_chairs.event_chairs_service_dep import EventChairServiceDep

event_chairs_router = APIRouter(prefix="/{event_id}/chairs", tags=["Events: Chairs"])


@event_chairs_router.get(path="", response_model=List[ChairResponseSchema], dependencies=[Depends(verify_is_organizer)])
async def read_event_chairs(chair_service: EventChairServiceDep, event_id: str):
    return await chair_service.get_all_chairs(event_id)


@event_chairs_router.post(path="", status_code=201, dependencies=[Depends(verify_is_organizer)])
async def invite_chair(chair_service: EventChairServiceDep, chair: ChairRequestSchema, event_id: str) -> str:
    return await chair_service.invite_chair(chair, event_id)


@event_chairs_router.patch(
    path="/accept",
    status_code=204,
    response_model=None,
    dependencies=[Depends(verify_user_exists)]
)
async def accept_chair_invitation(caller_id: CallerIdDep, event_id: str, chair_service: EventChairServiceDep):
    await chair_service.accept_chair_invitation(caller_id, event_id)


@event_chairs_router.delete(
    path="/{user_id}",
    status_code=201,
    response_model=None,
    dependencies=[Depends(verify_is_organizer)]
)
async def remove_chair(
        event_id: str,
        user_id: str,
        chair_service: EventChairServiceDep
) -> None:
    await chair_service.remove_chair(event_id, user_id)
