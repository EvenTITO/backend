from app.models.event import EventModel
from app.schemas.schemas import EventSchema
from app.organizers.exceptions import ExpirationDateException
from app.organizers.schemas import OrganizationsForUserSchema
from app.organizers.schemas import OrganizerInEventResponseSchema
from app.models.user import UserModel
from app.users.schemas import UserSchema
from ..models.organizer import InvitationStatus, OrganizerModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, func


async def is_organizer(
    db: AsyncSession, event_id: str, caller_id: str
):
    query = select(OrganizerModel).where(
        OrganizerModel.id_event == event_id,
        OrganizerModel.id_organizer == caller_id
    )
    result = await db.execute(query)
    return result.first() is not None


async def add_organizer_to_event(
    db: AsyncSession, id_organizer: str, id_event: str,
):
    new_organizer = OrganizerModel(
        id_organizer=id_organizer,
        id_event=id_event
    )
    db.add(new_organizer)
    await db.commit()
    await db.refresh(new_organizer)

    return new_organizer


async def get_organizer_in_event(
    db: AsyncSession,
    event_id: str,
    organizer_id: str
):
    query = select(OrganizerModel).where(
        OrganizerModel.id_event == event_id,
        OrganizerModel.id_organizer == organizer_id
    )
    result = await db.execute(query)
    return result.first()


async def get_organizers_in_event(db: AsyncSession, event_id: str):
    query = select(UserModel, OrganizerModel).where(
        OrganizerModel.id_event == event_id,
        OrganizerModel.id_organizer == UserModel.id
    )
    result = await db.execute(query)
    users_organizers = result.fetchall()
    response = []
    for user, organizer in users_organizers:
        response.append(OrganizerInEventResponseSchema(
            id_event=organizer.id_event,
            id_organizer=organizer.id_organizer,
            invitation_date=organizer.creation_date,
            organizer=UserSchema(
                email=user.email,
                name=user.name,
                lastname=user.lastname
            )
        ))
    return response


async def get_user_event_organizes(db: AsyncSession, user_id: str):
    query = select(EventModel, OrganizerModel).where(
        OrganizerModel.id_organizer == user_id,
        OrganizerModel.id_event == EventModel.id
    )
    result = await db.execute(query)
    events_organizer = result.fetchall()
    response = []
    for event, organizer in events_organizer:
        response.append(OrganizationsForUserSchema(
            id_event=organizer.id_event,
            id_organizer=organizer.id_organizer,
            invitation_date=organizer.creation_date,
            event=EventSchema(
                title=event.title,
                start_date=event.start_date,
                end_date=event.end_date,
                event_type=event.event_type,
                description=event.description,
                location=event.location,
                tracks=event.tracks,
            )
        ))
    return response


async def delete_organizer(
    db: AsyncSession,
    id_event,
    id_organizer
):
    organizer = await get_organizer_in_event(
        db,
        id_event,
        id_organizer
    )
    await db.delete(organizer)
    await db.commit()
    return organizer


async def update_invitation_status(
        db: AsyncSession,
        caller_id: str,
        event_id: str,
        status_modification: InvitationStatus):
    query = update(OrganizerModel).where(
        OrganizerModel.id_event == event_id,
        OrganizerModel.id_organizer == caller_id,
        OrganizerModel.invitation_expiration_date > func.now()
    ).values(invitation_status=status_modification)
    result = await db.execute(query)

    await db.commit()
    # Check if update was OK
    if result.rowcount < 1:
        raise ExpirationDateException()
