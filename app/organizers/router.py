from typing import List
from app.authorization.same_user_or_admin_dep import SameUserOrAdminDep
from app.database.session_dep import SessionDep
from app.repository import organizers_crud
from app.authorization.caller_id_dep import CallerIdDep
from .schemas import (
    ModifyInvitationStatusSchema,
    OrganizationsForUserSchema,
    OrganizerInEventResponseSchema,
    OrganizerRequestSchema
)
from fastapi import APIRouter
from app.routers.users.users import users_router
from app.routers.events.events import events_router
from app.organizers.dependencies import EventOrganizerDep

organizers_events_router = APIRouter(
    prefix=events_router.prefix + "/{event_id}" + '/organizers',
    tags=["Event Organizers"]
)

organizers_users_router = APIRouter(
    prefix=users_router.prefix + "/{user_id}" + '/organized-events',
    tags=["User Organizers"]
)




@organizers_events_router.patch("", status_code=200)
async def update_status_organizer(
    caller_id: CallerIdDep,
    event_id: str,
    _: EventOrganizerDep,
    status_modification: ModifyInvitationStatusSchema,
    db: SessionDep
):
    await organizers_crud.update_invitation_status(
        db,
        caller_id,
        event_id,
        status_modification.invitation_status
    )
    return


@organizers_users_router.get(
    "", response_model=List[OrganizationsForUserSchema]
)
async def read_user_event_organizes(
    user_id: str,
    _: SameUserOrAdminDep,
    db: SessionDep
):
    return await organizers_crud.get_user_event_organizes(db, user_id)


# @organizers_events_router.delete(
#     "/{organizer_id}",
#     status_code=204
# )
# async def delete_organizer(
#     event_id: str,
#     organizer_id: str,
#     caller_id: CallerIdDep,
#     db: SessionDep
# ):
#     validate_user_creator_or_organizer(db, event_id, caller_id)
#     organizer_in_event = OrganizerSchema(
#         id_organizer=organizer_id,
#         id_event=event_id
#     )

#     crud.delete_organizer(
#         db, organizer_in_event
#     )
