from app.utils.dependencies import SessionDep, CallerIdDep
from app.organizers import crud
from .schemas import OrganizerRequestSchema, OrganizerSchema
from fastapi import APIRouter
from app.utils.authorization import validate_user_creator_or_organizer


organizers_router = APIRouter(prefix="/organizers", tags=["Organizers"])


@organizers_router.post(
    "/{event_id}/",
    response_model=OrganizerSchema
)
def create_organizer(
    event_id: str,
    user: OrganizerRequestSchema,
    caller_id: CallerIdDep,
    db: SessionDep
):
    validate_user_creator_or_organizer(db, event_id, caller_id)

    new_organizer = OrganizerSchema(
        **user.model_dump(),
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
