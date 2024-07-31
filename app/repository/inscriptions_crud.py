from app.database.models.event import EventModel
from app.schemas.events.create_event import CreateEventSchema
from app.schemas.inscriptions.schemas import (
    InscriptionsForUserSchema,
    InscriptionsInEventResponseSchema
)
from app.database.models.user import UserModel
from app.schemas.users.user import UserSchema
from ..database.models.inscription import InscriptionModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_event_inscriptions(db, event_id):
    query = select(UserModel, InscriptionModel).where(
        InscriptionModel.event_id == event_id,
        InscriptionModel.inscriptor_id == UserModel.id
    )
    result = await db.execute(query)
    users_inscriptions = result.fetchall()
    response = []
    for user, inscription in users_inscriptions:
        response.append(InscriptionsInEventResponseSchema(
            event_id=inscription.event_id,
            inscriptor_id=inscription.inscriptor_id,
            status=inscription.status,
            creation_date=inscription.creation_date,
            inscripted_user=UserSchema(
                email=user.email,
                name=user.name,
                lastname=user.lastname
            )
        ))
    return response


async def user_already_inscribed(db, user_id, event_id):
    query = select(InscriptionModel).where(
        InscriptionModel.event_id == event_id,
        InscriptionModel.inscriptor_id == user_id
    )
    result = await db.execute(query)
    return result.first() is not None


async def inscribe_user_to_event(
        db: AsyncSession,
        event_id: str,
        inscriptor_id: str
):
    db_inscription = InscriptionModel(
        event_id=event_id,
        inscriptor_id=inscriptor_id
    )
    db.add(db_inscription)
    await db.commit()
    await db.refresh(db_inscription)
    return db_inscription


async def read_user_inscriptions(
    db: AsyncSession,
    user_id: str,
    offset: int,
    limit: int
):
    query = select(EventModel, InscriptionModel).where(
        InscriptionModel.inscriptor_id == user_id,
        InscriptionModel.event_id == EventModel.id
    ).offset(offset).limit(limit)
    result = await db.execute(query)
    events_inscription = result.fetchall()
    response = []
    for event, inscription in events_inscription:
        response.append(InscriptionsForUserSchema(
            event_id=inscription.event_id,
            inscriptor_id=inscription.inscriptor_id,
            status=inscription.status,
            creation_date=inscription.creation_date,
            event=CreateEventSchema(
                title=event.title,
                event_type=event.event_type,
                description=event.description,
                location=event.location,
                tracks=event.tracks,
            )
        ))
    return response


# # def delete_inscriptions_to_event(db: AsyncSession,
# caller_id: str, event_id: str):
#     validate_user_roles(db, caller_id)

#     inscriptions = get_event_inscriptions(db, event_id)
#     inscriptions_dicts = []
#     for inscription in inscriptions:
#         db.delete(inscription)
#         inscriptions_dicts.append(inscription.to_dict())

#     db.commit()

#     return GetInscriptionReplySchema(inscriptions=inscriptions_dicts)
