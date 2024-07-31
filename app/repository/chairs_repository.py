from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.chair import ChairModel
from app.database.models.member import InvitationStatus
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

    async def create_chair(self, event_id: str, chair_id: str, expiration_date: datetime, tracks: list[str]):
        db_in = ChairModel(
            user_id=chair_id,
            event_id=event_id,
            invitation_expiration_date=expiration_date,
            tracks=tracks
        )
        await self._create(db_in)
