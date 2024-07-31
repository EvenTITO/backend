from typing import List

from fastapi import APIRouter, Depends

from app.authorization.caller_id_dep import CallerIdDep
from app.authorization.organizer_or_admin_dep import verify_is_organizer
from app.authorization.user_id_dep import verify_user_exists
from app.schemas.members.member_schema import MemberRequestSchema, MemberResponseSchema, ModifyInvitationStatusSchema
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
    return await organizer_service.get_organizers(event_id)


@event_organizers_router.post(path="", status_code=201, dependencies=[Depends(verify_is_organizer)])
async def invite_organizer(
        organizer_service: EventOrganizersServiceDep,
        organizer: MemberRequestSchema,
        event_id: str
) -> str:
    return await organizer_service.invite_organizer(organizer, event_id)


@event_organizers_router.patch("", status_code=200, dependencies=[Depends(verify_user_exists)])
async def accept_or_decline_organizer_invitation(
        caller_id: CallerIdDep,
        event_id: str,
        organizer_service: EventOrganizersServiceDep,
        status_modification: ModifyInvitationStatusSchema,
):
    await organizer_service.update_invitation_status(
        caller_id,
        event_id,
        status_modification
    )
