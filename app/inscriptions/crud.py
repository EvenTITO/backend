from .model import InscriptionModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_event_inscriptions(db, event_id):
    query = select(InscriptionModel).where(
        InscriptionModel.id_event == event_id
    )
    result = await db.execute(query)
    return result.scalars().all()


async def user_already_inscribed(db, user_id, event_id):
    query = select(InscriptionModel).where(
        InscriptionModel.id_event == event_id,
        InscriptionModel.id_inscriptor == user_id
    )
    result = await db.execute(query)
    return result.first() is not None


async def inscribe_user_to_event(
        db: AsyncSession,
        id_event: str,
        id_inscriptor: str
):
    db_inscription = InscriptionModel(
        id_event=id_event,
        id_inscriptor=id_inscriptor
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
    query = select(InscriptionModel).where(
        InscriptionModel.id_inscriptor == user_id
    ).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


# # def delete_inscriptions_to_event(db: AsyncSession, caller_id: str, event_id: str):
#     validate_user_permissions(db, caller_id)

#     inscriptions = get_event_inscriptions(db, event_id)
#     inscriptions_dicts = []
#     for inscription in inscriptions:
#         db.delete(inscription)
#         inscriptions_dicts.append(inscription.to_dict())

#     db.commit()

#     return GetInscriptionReplySchema(inscriptions=inscriptions_dicts)
