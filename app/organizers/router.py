from typing import List
from app.users.dependencies import SameUserOrAdminDep
from app.database.dependencies import SessionDep
from app.organizers import crud
from .schemas import OrganizerRequestSchema, OrganizerSchema
from fastapi import APIRouter
from app.users.router import users_router
from app.events.router import events_router
from app.organizers.dependencies import EventOrganizerDep
from app.users.utils import get_user

organizers_events_router = APIRouter(
    prefix=events_router.prefix + "/{event_id}" + '/organizers',
    tags=["Event Organizers"]
)

organizers_users_router = APIRouter(
    prefix=users_router.prefix + "/{user_id}" + '/organized-events',
    tags=["User Organizers"]
)


@organizers_events_router.post("", status_code=201)
async def create_organizer(
    event_id: str,
    _: EventOrganizerDep,
    organizer: OrganizerRequestSchema,
    db: SessionDep
) -> str:
    organizer_user = await get_user(db, organizer.id_organizer)
    organizer = await crud.add_organizer_to_event(
        db,
        organizer_user.id,
        event_id
    )
    return organizer.id_organizer


@organizers_events_router.get(
    "", response_model=List[OrganizerSchema]
)
async def read_event_organizers(
    event_id: str,
    _: EventOrganizerDep,
    db: SessionDep
):
    return await crud.get_organizers_in_event(db, event_id)


@organizers_users_router.get(
    "", response_model=List[OrganizerSchema]
)
async def read_user_event_organizes(
    user_id: str,
    _: SameUserOrAdminDep,
    db: SessionDep
):
    return await crud.get_user_event_organizes(db, user_id)


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
