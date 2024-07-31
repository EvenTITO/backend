from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.organizer import OrganizerModel
from app.repository.members_repository import MemberRepository


class OrganizerRepository(MemberRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrganizerModel)

    async def _primary_key_conditions(self, primary_key):
        event_id, organizer_id = primary_key
        return [
            OrganizerModel.event_id == event_id,
            OrganizerModel.user_id == organizer_id
        ]

    async def get_organizer(self, event_id, user_id):
        return await self.get((event_id, user_id))

    async def create_organizer(self, event_id: str, organizer_id: str, expiration_date: datetime):
        db_in = OrganizerModel(
            user_id=organizer_id,
            event_id=event_id,
            invitation_expiration_date=expiration_date
        )
        await self._create(db_in)
