from app.utils.dependencies import SessionDep, CallerIdDep
from app.organizers import crud
from .schemas import OrganizerRequestSchema, OrganizerSchema
from fastapi import APIRouter
from app.users.router import users_router
from app.events.router import events_router
from app.utils.authorization import validate_user_creator_or_organizer


ORGANIZERS_PREFIX = '/organizers'

organizers_events_router = APIRouter(
    prefix=events_router.prefix+"/{event_id}"+ORGANIZERS_PREFIX,
    tags=["Event Suscriptions"]
)

suscriptions_users_router = APIRouter(
    prefix=users_router.prefix+"/{user_id}"+ORGANIZERS_PREFIX,
    tags=["User Suscriptions"]
)


@organizers_events_router.post("", status_code=201)
def create_organizer(
    event_id: str,
    organizer: OrganizerRequestSchema,
    caller_id: CallerIdDep,
    db: SessionDep
) -> str:
    validate_user_creator_or_organizer(db, event_id, caller_id)

    new_organizer = OrganizerSchema(
        **organizer.model_dump(),
        id_event=event_id
    )

    return crud.add_organizer_to_event(
        db, new_organizer
    )


# @organizers_router.delete(
#     "/{event_id}/",
#     response_model=OrganizerSchema
# )
# def delete_organizer(
#     event_id: str,
#     user: OrganizerRequestSchema,
#     caller_id: CallerIdDep,
#     db: SessionDep
# ):
#     validate_user_creator_or_organizer(db, event_id, caller_id)
#     organizer_in_event = OrganizerSchema(
#         **user.model_dump(),
#         id_event=event_id
#     )

#     return crud.delete_organizer(
#         db, organizer_in_event
#     )


# @organizers_router.get(
#     "/events/{event_id}/", response_model=GetSuscriptionReplySchema
# )
# def read_event_suscriptions(event_id: str, db: SessionDep):
#     return crud.read_event_suscriptions(db, event_id)


# @organizers_router.get(
#     "/users", response_model=GetSuscriptionReplySchema
# )
# def read_user_suscriptions(
#     caller_id: CallerIdDep,
#     db: SessionDep,
#     offset: int = 0,
#     limit: int = Query(default=100, le=100)
# ):
#     return crud.read_user_suscriptions(db, caller_id, offset, limit)
