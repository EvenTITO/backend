from typing import List
from fastapi import APIRouter, Depends
from app.authorization.caller_id_dep import CallerIdDep
from app.schemas.members.chair_schema import ChairRequestSchema
from app.schemas.members.member_schema import MemberResponseSchema, ModifyInvitationStatusSchema
from app.authorization.organizer_or_admin_dep import verify_is_organizer
from app.authorization.user_id_dep import verify_user_exists
from app.services.event_organizers.event_organizers_service_dep import EventOrganizersServiceDep

event_chairs_router = APIRouter(
    prefix="/{event_id}/chairs",
    tags=["Events: Chairs"]
)


@event_chairs_router.post(path="", status_code=201, dependencies=[Depends(verify_is_organizer)])
async def invite_chair(
    service: EventOrganizersServiceDep,
    chair: ChairRequestSchema,
    event_id: str,
) -> str:
    return await service.invite(chair, event_id)


@event_chairs_router.get(
    path="",
    response_model=List[ChairRequestSchema],
    dependencies=[Depends(verify_is_organizer)],
)
async def read_event_chairs(
    service: EventOrganizersServiceDep,
    event_id: str,
):
    return await service.get_organizers(event_id)


@event_chairs_router.patch("", status_code=200, dependencies=[Depends(verify_user_exists)])
async def accept_or_decline_chair_invitation(
    caller_id: CallerIdDep,
    event_id: str,
    service: EventOrganizersServiceDep,
    status_modification: ModifyInvitationStatusSchema,
):
    await service.update_invitation_status(
        caller_id,
        event_id,
        status_modification
    )

