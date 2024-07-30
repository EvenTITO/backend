from typing import List
from fastapi import APIRouter, Depends
from app.authorization.caller_id_dep import CallerIdDep
from app.schemas.members.organizers.organizer_schema import ModifyInvitationStatusSchema, OrganizerInEventResponseSchema, OrganizerRequestSchema
from app.authorization.organizer_or_admin_dep import verify_is_organizer
from app.authorization.user_id_dep import verify_user_exists
from app.services.event_organizers.event_organizers_service_dep import EventOrganizersServiceDep

event_organizers_router = APIRouter(
    prefix="/{event_id}/organizers",
    tags=["Events: Organizers"]
)


@event_organizers_router.post("", status_code=201, dependencies=[Depends(verify_is_organizer)])
async def invite_organizer(
    service: EventOrganizersServiceDep,
    organizer: OrganizerRequestSchema,
    event_id: str,
) -> str:
    return await service.invite(organizer, event_id)


@event_organizers_router.get(
    "",
    response_model=List[OrganizerInEventResponseSchema],
    dependencies=[Depends(verify_is_organizer)],
)
async def read_event_organizers(
    service: EventOrganizersServiceDep,
    event_id: str,
):
    return await service.get_organizers(event_id)


@event_organizers_router.patch("", status_code=200, dependencies=[Depends(verify_user_exists)],)
async def accept_or_decline_organizer_invitation(
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

