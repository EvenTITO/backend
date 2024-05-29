from sqlalchemy.future import select
from .model import OrganizerModel
from .schemas import OrganizerSchema
from sqlalchemy.ext.asyncio import AsyncSession


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
    query = select(OrganizerModel).where(
        OrganizerModel.id_event == event_id
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_user_event_organizes(db: AsyncSession, user_id: str):
    query = select(OrganizerModel).where(
        OrganizerModel.id_organizer == user_id
    )
    result = await db.execute(query)
    return result.scalars().all()


async def delete_organizer(
    db: AsyncSession, organizer_to_delete: OrganizerSchema
):
    organizer = await get_organizer_in_event(
        db,
        organizer_to_delete.id_event,
        organizer_to_delete.id_organizer
    )
    await db.delete(organizer)
    await db.commit()
    return organizer
