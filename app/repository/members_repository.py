from datetime import datetime

from sqlalchemy import update, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.member import InvitationStatus
from app.database.models.user import UserModel
from app.repository.crud_repository import Repository


class MemberRepository(Repository):
    def __init__(self, session: AsyncSession, model):
        super().__init__(session, model)

    async def get_all(self, event_id: str):
        query = select(UserModel, self.model).where(
            and_(
                self.model.event_id == event_id,
                self.model.user_id == UserModel.id
            )
        )
        result = await self.session.execute(query)
        return result.fetchall()

    async def get_all_by_status(self, event_id: str, status: InvitationStatus):
        query = select(UserModel, self.model).where(
            and_(
                self.model.event_id == event_id,
                self.model.user_id == UserModel.id,
                self.model.invitation_status == status
            )
        )
        result = await self.session.execute(query)
        return result.fetchall()

    async def has_invitation_pending(self, event_id: str, user_id: str):
        member = await self.get((event_id, user_id))
        return member is not None and member.invitation_status == InvitationStatus.INVITED

    async def has_invitation_or_is_member(self, event_id: str, user_id: str):
        return await self.exists((event_id, user_id))

    async def update_expiration_date(self, event_id: str, user_id: str, expiration_date: datetime):
        query = (update(self.model)
                 .where(and_(self.model.user_id == user_id, self.model.event_id == event_id))
                 .values(expiration_date=expiration_date))
        await self.session.execute(query)
        return await self.session.commit()

    async def accept_invitation(self, event_id: str, user_id: str):
        query = (update(self.model)
                 .where(and_(self.model.user_id == user_id, self.model.event_id == event_id))
                 .values(invitation_status=InvitationStatus.ACCEPTED))
        await self.session.execute(query)
        return await self.session.commit()

    async def remove_member(self, event_id, user_id):
        return await self.remove((event_id, user_id))
