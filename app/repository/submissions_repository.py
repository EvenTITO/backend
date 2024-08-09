from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.submission import SubmissionModel
from app.repository.crud_repository import Repository


class SubmissionsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, SubmissionModel)

    async def do_submit(self, event_id, work_id):

