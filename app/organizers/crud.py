from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from .model import OrganizerModel
from .schemas import OrganizerSchema
from sqlalchemy.ext.asyncio import AsyncSession

EVENT_ORGANIZER_NOT_FOUND = "Event organizer not found."


def handle_database_organizer_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(
                status_code=404, detail=EVENT_ORGANIZER_NOT_FOUND)

    return wrapper


async def is_organizer(
    db: AsyncSession, event_id: str, caller_id: str
):
    query = select(OrganizerModel).where(
        OrganizerModel.id_event == event_id,
        OrganizerModel.id_organizer == caller_id
    )
    result = await db.execute(query)
    return result.first() is not None


@handle_database_organizer_error
async def add_organizer_to_event(
    db: AsyncSession, new_organizer: OrganizerSchema
):
    new_organizer = OrganizerModel(**new_organizer.model_dump())
    db.add(new_organizer)
    db.commit()
    db.refresh(new_organizer)

    return new_organizer


@handle_database_organizer_error
async def get_organizer_in_event(
    db: AsyncSession,
    event_id: str,
    organizer_id: str
):
    return (
        db
        .query(OrganizerModel)
        .filter(
            OrganizerModel.id_event == event_id,
            OrganizerModel.id_organizer == organizer_id
        ).one()
    )


@handle_database_organizer_error
async def get_organizers_in_event(db: AsyncSession, event_id: str):
    return (
        db
        .query(OrganizerModel)
        .filter(
            OrganizerModel.id_event == event_id
        ).all()
    )


@handle_database_organizer_error
async def get_user_event_organizes(db: AsyncSession, user_id: str):
    return (
        db
        .query(OrganizerModel)
        .filter(
            OrganizerModel.id_organizer == user_id
        ).all()
    )


@handle_database_organizer_error
async def delete_organizer(
    db: AsyncSession, organizer_to_delete: OrganizerSchema
):
    organizer = get_organizer_in_event(
        db,
        organizer_to_delete.id_event,
        organizer_to_delete.id_organizer
    )
    db.delete(organizer)
    db.commit()
    return organizer
