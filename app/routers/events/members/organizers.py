from fastapi import APIRouter, Depends
from app.organizers.schemas import OrganizerRequestSchema
from app.authorization.organizer_or_admin_dep import verify_is_organizer
from app.services.event_organizers.event_organizers_service_dep import EventOrganizersServiceDep

event_organizers_router = APIRouter(
    prefix="/{event_id}/organizers",
    tags=["Events: Organizers"]
)


@event_organizers_router.post("", status_code=201, dependencies=[Depends(verify_is_organizer)])
async def invite_organizer(
    service: EventOrganizersServiceDep,
    organizer: OrganizerRequestSchema,
) -> str:
    return await service.invite(organizer)

# @event_organizers_router.get(
#     "", response_model=List[OrganizerInEventResponseSchema]
# )
# async def read_event_organizers(
#     event_id: str,
#     _: EventOrganizerDep,
#     db: SessionDep
# ):
#     return await organizers_crud.get_organizers_in_event(db, event_id)


# @event_organizers_router.patch("", status_code=200)
# async def update_status_organizer(
#     caller_id: CallerIdDep,
#     event_id: str,
#     _: EventOrganizerDep,
#     status_modification: ModifyInvitationStatusSchema,
#     db: SessionDep
# ):
#     await organizers_crud.update_invitation_status(
#         db,
#         caller_id,
#         event_id,
#         status_modification.invitation_status
#     )
#     return
