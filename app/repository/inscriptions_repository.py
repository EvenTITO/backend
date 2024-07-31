from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.inscription import InscriptionModel
from app.database.models.user import UserModel
from app.repository.crud_repository import Repository
from app.schemas.inscriptions.schemas import InscriptionsInEventResponseSchema
from app.schemas.users.user import UserSchema


class InscriptionsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, InscriptionModel)

    async def _primary_key_conditions(self, primary_key):
        event_id, inscriptor_id = primary_key
        return [
            InscriptionModel.event_id == event_id,
            InscriptionModel.inscriptor_id == inscriptor_id
        ]

    async def inscription_exists(self, event_id: str, inscriptor_id: str):
        return await self.exists((event_id, inscriptor_id))

    async def inscribe(self, event_id: str, inscriptor_id: str):
        db_inscription = InscriptionModel(
            event_id=event_id,
            inscriptor_id=inscriptor_id
        )
        await self._create(db_inscription)

    async def get_event_inscriptions(self, event_id: str):
        # TODO: mejorar query. No deberia ir a este repository, sino pasar por este
        # repository para buscar ids, y luego ir a users_service para buscar
        # usuarios.
        query = select(UserModel, InscriptionModel).where(
            InscriptionModel.event_id == event_id,
            InscriptionModel.inscriptor_id == UserModel.id
        )
        result = await self.session.execute(query)
        users_inscriptions = result.fetchall()
        response = []
        for user, inscription in users_inscriptions:
            response.append(InscriptionsInEventResponseSchema(
                event_id=inscription.event_id,
                inscriptor_id=inscription.inscriptor_id,
                status=inscription.status,
                creation_date=inscription.creation_date,
                inscripted_user=UserSchema(
                    email=user.email,
                    name=user.name,
                    lastname=user.lastname
                )
            ))
        return response
