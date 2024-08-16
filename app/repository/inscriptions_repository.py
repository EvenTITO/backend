from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.inscription import InscriptionModel
from app.repository.crud_repository import Repository
from app.schemas.inscriptions.inscription import InscriptionRequestSchema


class InscriptionsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, InscriptionModel)

    async def inscription_exists(self, event_id: str, user_id: str):
        conditions = [InscriptionModel.event_id == event_id, InscriptionModel.user_id == user_id]
        return await self._exists_with_conditions(conditions)

    async def inscribe(self, event_id: str, user_id: str, inscription: InscriptionRequestSchema) -> InscriptionModel:
        db_inscription = InscriptionModel(
            event_id=event_id,
            user_id=user_id,
            roles=inscription.roles,
            affiliation=inscription.affiliation
        )
        return await self._create(db_inscription)


"""
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
        return response """
