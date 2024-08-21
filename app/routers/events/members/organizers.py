from typing import List

from fastapi import APIRouter, Depends

from app.authorization.organizer_or_admin_dep import verify_is_organizer
from app.schemas.members.member_schema import MemberResponseSchema
from app.services.event_organizers.event_organizers_service_dep import EventOrganizersServiceDep

event_organizers_router = APIRouter(
    prefix="/{event_id}/organizers",
    tags=["Events: Organizers"]
)


@event_organizers_router.get(
    path="",
    response_model=List[MemberResponseSchema],
    dependencies=[Depends(verify_is_organizer)]
)
async def read_event_organizers(organizer_service: EventOrganizersServiceDep, event_id: str):
    return await organizer_service.get_all_organizers(event_id)


@event_organizers_router.delete(
    path="/{user_id}",
    status_code=201,
    response_model=None,
    dependencies=[Depends(verify_is_organizer)]
)
async def remove_organizer(
        event_id: str,
        user_id: str,
        organizer_service: EventOrganizersServiceDep
) -> None:
    await organizer_service.remove_organizer(event_id, user_id)
