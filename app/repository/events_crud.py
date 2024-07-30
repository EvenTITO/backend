from ..database.models.event import EventModel
from sqlalchemy.ext.asyncio import AsyncSession


async def get_event_by_id(db: AsyncSession, event_id: str):
    event = await db.get(EventModel, event_id)
    return event
