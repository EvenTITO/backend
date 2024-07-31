from datetime import datetime

from sqlalchemy import select
from app.database.models.organizer import OrganizerModel
from app.database.models.user import UserModel
from app.schemas.members.member_schema import MemberResponseSchema, ModifyInvitationStatusSchema
from app.repository.crud_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users.user import UserSchema


class OrganizersRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrganizerModel)

    async def is_organizer(self, event_id: str, organizer_id: str):
        return await self.exists((event_id, organizer_id))

    async def get_organizer(self, event_id, organizer_id):
        return await self.get((event_id, organizer_id))

    async def _primary_key_conditions(self, primary_key):
        event_id, organizer_id = primary_key
        return [
            OrganizerModel.event_id == event_id,
            OrganizerModel.organizer_id == organizer_id
        ]

    async def create_organizer(self, event_id: str, organizer_id: str, expiration_date: datetime):
        db_in = OrganizerModel(
            organizer_id=organizer_id,
            event_id=event_id,
            invitation_expiration_date=expiration_date
        )
        await self._create(db_in)

    async def update_invitation(
        self,
        event_id: str,
        organizer_id: str,
        status_modification: ModifyInvitationStatusSchema
    ):
        return await self.update((event_id, organizer_id), status_modification)

    async def get_event_organizers(self, event_id: str):
        # TODO: va aca o a otro repository? Agregar limit offset, o limitar las invitaciones.
        query = select(UserModel, OrganizerModel).where(
            OrganizerModel.event_id == event_id,
            OrganizerModel.organizer_id == UserModel.id
        )
        result = await self.session.execute(query)
        users_organizers = result.fetchall()
        response = []
        for user, organizer in users_organizers:
            response.append(MemberResponseSchema(
                event_id=organizer.event_id,
                user_id=organizer.organizer_id,
                invitation_date=organizer.creation_date,
                user=UserSchema(
                    email=user.email,
                    name=user.name,
                    lastname=user.lastname
                )
            ))
        return response
