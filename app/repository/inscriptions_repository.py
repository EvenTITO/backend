from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.inscription import InscriptionModel
from app.repository.crud_repository import Repository


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
