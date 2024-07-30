from datetime import datetime

from sqlalchemy import select
from app.database.models.organizer import OrganizerModel
from app.database.models.user import UserModel
from app.schemas.organizers.schemas import ModifyInvitationStatusSchema, OrganizerInEventResponseSchema
from app.repository.crud_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users.user import UserSchema


class OrganizersRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrganizerModel)

    async def is_organizer(self, id_event: str, id_organizer: str):
        return await self.exists((id_event, id_organizer))

    async def get_organizer(self, id_event, id_organizer):
        return await self.get((id_event, id_organizer))

    async def _primary_key_conditions(self, primary_key):
        id_event, id_organizer = primary_key
        return [
            OrganizerModel.id_event == id_event,
            OrganizerModel.id_organizer == id_organizer
        ]

    async def create(self, id_event: str, id_organizer: str, expiration_date: datetime):
        db_in = OrganizerModel(
            id_organizer=id_organizer,
            id_event=id_event,
            invitation_expiration_date=expiration_date
        )
        await self._create(db_in)

    async def update_invitation(
        self,
        id_event: str,
        id_organizer: str,
        status_modification: ModifyInvitationStatusSchema
    ):
        return await self.update((id_event, id_organizer), status_modification)

    async def get_event_organizers(self, id_event: str):
        # TODO: va aca o a otro repository? Agregar limit offset, o limitar las invitaciones.
        query = select(UserModel, OrganizerModel).where(
            OrganizerModel.id_event == id_event,
            OrganizerModel.id_organizer == UserModel.id
        )
        result = await self.session.execute(query)
        users_organizers = result.fetchall()
        response = []
        for user, organizer in users_organizers:
            response.append(OrganizerInEventResponseSchema(
                id_event=organizer.id_event,
                id_organizer=organizer.id_organizer,
                invitation_date=organizer.creation_date,
                organizer=UserSchema(
                    email=user.email,
                    name=user.name,
                    lastname=user.lastname
                )
            ))
        return response
