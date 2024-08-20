from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.chair import ChairModel
from app.repository.members_repository import MemberRepository


class ChairRepository(MemberRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChairModel)

    async def _primary_key_conditions(self, primary_key):
        event_id, chair_id = primary_key
        return [
            ChairModel.event_id == event_id,
            ChairModel.user_id == chair_id
        ]

    async def get_chair(self, event_id, user_id):
        return await self.get((event_id, user_id))
