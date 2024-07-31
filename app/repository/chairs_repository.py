from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.chair import ChairModel
from app.database.models.user import UserModel
from app.repository.members_repository import MemberRepository
from app.schemas.members.member_schema import ModifyInvitationStatusSchema


class ChairRepository(MemberRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChairModel)

    async def get_all_chairs(self, event_id: str):
        query = select(UserModel, ChairModel).where(
            ChairModel.event_id == event_id,
            ChairModel.user_id == UserModel.id
        )
        result = await self.session.execute(query)
        return result.fetchall()

    async def get_all_chairs_by_status(self, event_id: str, status: str):
        query = select(UserModel, ChairModel).where(
            ChairModel.event_id == event_id,
            ChairModel.user_id == UserModel.id,
            ChairModel.invitation_status == status
        )
        result = await self.session.execute(query)
        return result.fetchall()

    #TODO aca para abajo
    async def get_chair(self, event_id, chair_id):
        return await self.get((event_id, chair_id))

    async def _primary_key_conditions(self, primary_key):
        event_id, chair_id = primary_key
        return [
            ChairModel.event_id == event_id,
            ChairModel.user_id == chair_id
        ]

    async def create_chair(self, event_id: str, chair_id: str, expiration_date: datetime, tracks: list[str]):
        db_in = ChairModel(
            user_id=chair_id,
            event_id=event_id,
            invitation_expiration_date=expiration_date,
            tracks=tracks
        )
        await self._create(db_in)

    async def update_invitation(
            self,
            event_id: str,
            chair_id: str,
            status_modification: ModifyInvitationStatusSchema
    ):
        return await self.update((event_id, chair_id), status_modification)
