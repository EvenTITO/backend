from app.database.models.organizer import OrganizerModel
from app.repository.crud_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession


class OrganizersRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrganizerModel)

    async def is_organizer(self, id_event: str, id_organizer: str):
        return await self.exists((id_event, id_organizer))

    async def _primary_key_conditions(self, primary_key):
        id_event, id_organizer = primary_key
        return [
            OrganizerModel.id_event == id_event,
            OrganizerModel.id_organizer == id_organizer
        ]
