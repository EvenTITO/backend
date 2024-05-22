from typing import List
from app.utils.dependencies import SessionDep, CallerIdDep
from app.organizers import crud
from .schemas import OrganizerRequestSchema, OrganizerSchema
from fastapi import APIRouter
from app.users.router import users_router
from app.events.router import events_router
from app.utils.authorization import (
    validate_user_creator_or_organizer,
    validate_same_user_or_superuser
)


ORGANIZERS_PREFIX = '/organizers'

organizers_events_router = APIRouter(
    prefix=events_router.prefix+"/{event_id}"+ORGANIZERS_PREFIX,
    tags=["Event Organizers"]
)

organizers_users_router = APIRouter(
    prefix=users_router.prefix+"/{user_id}"+ORGANIZERS_PREFIX,
    tags=["User Organizers"]
)


@organizers_events_router.post("", status_code=201)
def create_organizer(
    event_id: str,
    organizer: OrganizerRequestSchema,
    caller_id: CallerIdDep,
    db: SessionDep
) -> str:
    validate_user_creator_or_organizer(db, event_id, caller_id)

    organizer = crud.add_organizer_to_event(
        db,
        OrganizerSchema(
            **organizer.model_dump(),
            id_event=event_id
        )
    )
    return organizer.id_organizer


@organizers_events_router.get(
    "", response_model=List[OrganizerSchema]
)
def read_event_organizers(
    event_id: str,
    caller_id: CallerIdDep,
    db: SessionDep
):
    validate_user_creator_or_organizer(db, event_id, caller_id)
    return crud.get_organizers_in_event(db, event_id)


@organizers_users_router.get(
    "", response_model=List[OrganizerSchema]
)
def read_user_event_organizes(
    user_id: str,
    caller_id: CallerIdDep,
    db: SessionDep
):
    validate_same_user_or_superuser(db, user_id, caller_id)
    return crud.get_user_event_organizes(db, user_id)


@organizers_events_router.delete(
    "/{organizer_id}",
    status_code=204
)
def delete_organizer(
    event_id: str,
    organizer_id: str,
    caller_id: CallerIdDep,
    db: SessionDep
):
    validate_user_creator_or_organizer(db, event_id, caller_id)
    organizer_in_event = OrganizerSchema(
        id_organizer=organizer_id,
        id_event=event_id
    )

    crud.delete_organizer(
        db, organizer_in_event
    )
