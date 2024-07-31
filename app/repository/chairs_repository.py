from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.chair import ChairModel
from app.database.models.user import UserModel
from app.repository.crud_repository import Repository
from app.schemas.members.member_schema import MemberResponseSchema, ModifyInvitationStatusSchema
from app.schemas.users.user import UserSchema


class ChairRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChairModel)

    async def is_chair(self, event_id: str, chair_id: str):
        return await self.exists((event_id, chair_id))

    async def get_chair(self, event_id, chair_id):
        return await self.get((event_id, chair_id))

    async def _primary_key_conditions(self, primary_key):
        event_id, chair_id = primary_key
        return [
            ChairModel.event_id == event_id,
            ChairModel.chair_id == chair_id
        ]

    async def create_chair(self, event_id: str, chair_id: str, expiration_date: datetime):
        db_in = ChairModel(
            chair_id=chair_id,
            event_id=event_id,
            invitation_expiration_date=expiration_date
        )
        await self._create(db_in)

    async def update_invitation(
            self,
            event_id: str,
            chair_id: str,
            status_modification: ModifyInvitationStatusSchema
    ):
        return await self.update((event_id, chair_id), status_modification)

    async def get_event_chairs(self, event_id: str):
        query = select(UserModel, ChairModel).where(
            ChairModel.event_id == event_id,
            ChairModel.chair_id == UserModel.id
        )
        result = await self.session.execute(query)
        users_chairs = result.fetchall()
        response = []
        for user, chair in users_chairs:
            response.append(MemberResponseSchema(
                event_id=chair.event_id,
                user_id=chair.chair_id,
                invitation_date=chair.creation_date,
                user=UserSchema(
                    email=user.email,
                    name=user.name,
                    lastname=user.lastname
                )
            ))
        return response
