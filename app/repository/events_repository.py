from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.event import EventModel
from app.repository.crud_repository import Repository


class EventsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EventModel)

    async def get_status(self, event_id: str):
        conditions = await self._primary_key_conditions(event_id)
        event_status = await self._get_with_values(conditions, EventModel.status)
        return event_status
