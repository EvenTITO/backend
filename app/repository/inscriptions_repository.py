from uuid import UUID
from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.inscription import InscriptionModel, InscriptionStatus
from app.repository.crud_repository import Repository
from app.schemas.inscriptions.inscription import InscriptionRequestSchema
from app.schemas.users.utils import UID


class InscriptionsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, InscriptionModel)

    async def inscription_exists(self, event_id: UUID, user_id: UID):
        conditions = [InscriptionModel.event_id == event_id, InscriptionModel.user_id == user_id]
        return await self._exists_with_conditions(conditions)

    async def inscribe(self, event_id: UUID, user_id: UID, inscription: InscriptionRequestSchema) -> InscriptionModel:
        db_inscription = InscriptionModel(
            event_id=event_id,
            user_id=user_id,
            roles=inscription.roles,
            affiliation=inscription.affiliation
        )
        return await self._create(db_inscription)

    async def get_event_inscriptions(self, event_id: UUID, offset: int, limit: int) -> list[InscriptionModel]:
        query = select(InscriptionModel).where(InscriptionModel.event_id == event_id).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_user_inscriptions(self, user_id: UID, offset: int, limit: int) -> list[InscriptionModel]:
        query = select(InscriptionModel).where(InscriptionModel.user_id == user_id).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_event_user_inscriptions(
            self,
            event_id: UUID,
            user_id: UID,
            offset: int,
            limit: int
    ) -> list[InscriptionModel]:
        query = (select(InscriptionModel)
                 .where(and_(InscriptionModel.user_id == user_id, InscriptionModel.event_id == event_id))
                 .offset(offset)
                 .limit(limit))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_user_inscription_by_id(self, user_id: UID, inscription_id: UUID) -> InscriptionModel:
        query = select(InscriptionModel).where(
            and_(InscriptionModel.id == inscription_id, InscriptionModel.user_id == user_id))
        result = await self.session.execute(query)
        return result.scalars().first()

    async def pay(self, inscription_id: UUID) -> None:
        update_query = (
            update(InscriptionModel).where(InscriptionModel.id == inscription_id).values(
                status=InscriptionStatus.PAYMENT_MADE.value())
        )
        await self.session.execute(update_query)
        await self.session.commit()
