from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.chair import ChairModel
from app.database.models.user import UserModel
from app.repository.crud_repository import Repository
from app.schemas.members.member_schema import MemberResponseSchema, ModifyInvitationStatusSchema
from app.schemas.users.user import UserSchema


class ChairsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChairModel)

    async def is_chair(self, id_event: str, id_chair: str):
        return await self.exists((id_event, id_chair))

    async def get_chair(self, id_event, id_chair):
        return await self.get((id_event, id_chair))

    async def _primary_key_conditions(self, primary_key):
        id_event, id_chair = primary_key
        return [
            ChairModel.id_event == id_event,
            ChairModel.id_chair == id_chair
        ]

    async def create_organizer(self, id_event: str, id_chair: str, expiration_date: datetime):
        db_in = ChairModel(
            id_chair=id_chair,
            id_event=id_event,
            invitation_expiration_date=expiration_date
        )
        await self._create(db_in)

    async def update_invitation(
            self,
            id_event: str,
            id_chair: str,
            status_modification: ModifyInvitationStatusSchema
    ):
        return await self.update((id_event, id_chair), status_modification)

    async def get_event_organizers(self, id_event: str):
        query = select(UserModel, ChairModel).where(
            ChairModel.id_event == id_event,
            ChairModel.id_chair == UserModel.id
        )
        result = await self.session.execute(query)
        users_chairs = result.fetchall()
        response = []
        for user, chair in users_chairs:
            response.append(MemberResponseSchema(
                id_event=chair.id_event,
                id_user=chair.id_chair,
                invitation_date=chair.creation_date,
                user=UserSchema(
                    email=user.email,
                    name=user.name,
                    lastname=user.lastname
                )
            ))
        return response
